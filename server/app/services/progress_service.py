from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.progress import UserProgress
from app.models.question import QuestionAttempt
from app.models.session import InterviewSession
from app.schemas.progress import ProgressResponse, DashboardData, RoadmapItem, TopicScore
from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional

async def get_or_create_progress(db: AsyncSession, user_id: int) -> UserProgress:
    result = await db.execute(select(UserProgress).where(UserProgress.user_id == user_id))
    progress = result.scalars().first()
    
    if not progress:
        progress = UserProgress(
            user_id=user_id,
            total_sessions=0,
            total_problems_solved=0,
            total_problems_attempted=0,
            current_streak=0,
            longest_streak=0,
            topic_scores={},
            difficulty_distribution={"easy": 0, "medium": 0, "hard": 0},
            weak_topics=[],
            strong_topics=[],
            roadmap=[]
        )
        db.add(progress)
        await db.commit()
        await db.refresh(progress)
        
    return progress

def calculate_weak_topics(topic_scores: Dict[str, Dict[str, Any]]) -> List[str]:
    weaks = []
    for topic, stats in topic_scores.items():
        attempted = stats.get("attempted", 0)
        solved = stats.get("solved", 0)
        avg_score = stats.get("avg_score", 0.0)
        # Weak if attempted > 0 and (solved/attempted < 0.6 or avg_score < 70)
        if attempted > 0:
            success_rate = solved / attempted
            if success_rate < 0.6 or avg_score < 70.0:
                weaks.append(topic)
    return weaks

def calculate_strong_topics(topic_scores: Dict[str, Dict[str, Any]]) -> List[str]:
    strongs = []
    for topic, stats in topic_scores.items():
        attempted = stats.get("attempted", 0)
        solved = stats.get("solved", 0)
        avg_score = stats.get("avg_score", 0.0)
        # Strong if solved >= 2 and success rate >= 80% and avg_score >= 80
        if attempted > 0:
            success_rate = solved / attempted
            if solved >= 2 and success_rate >= 0.8 and avg_score >= 80.0:
                strongs.append(topic)
    return strongs

def generate_roadmap(topic_scores: Dict[str, Dict[str, Any]], weak_topics: List[str]) -> List[Dict[str, Any]]:
    roadmap = []
    all_topics = ["arrays", "strings", "linked_lists", "trees", "graphs", "dynamic_programming", "sorting", "searching", "stacks_queues", "heaps"]
    
    # Priority 1: Weak topics
    for topic in weak_topics:
        stats = topic_scores.get(topic, {"solved": 0, "attempted": 0, "avg_score": 0.0})
        roadmap.append({
            "topic": topic,
            "priority": "high",
            "reason": f"Your current success rate is low (avg score: {stats.get('avg_score', 0):.1f}%). Focus on base exercises.",
            "suggested_count": 3,
            "difficulty": "easy" if stats.get("avg_score", 0) < 50 else "medium"
        })
        
    # Priority 2: Unattempted topics
    unattempted = [t for t in all_topics if t not in topic_scores or topic_scores[t].get("attempted", 0) == 0]
    for topic in unattempted[:3]:  # limit to 3 recommendations
        roadmap.append({
            "topic": topic,
            "priority": "medium",
            "reason": "You haven't attempted this topic yet. Start practicing to broaden your algorithm coverage.",
            "suggested_count": 2,
            "difficulty": "easy"
        })
        
    # Priority 3: Level up strong topics
    strong_topics = calculate_strong_topics(topic_scores)
    for topic in strong_topics[:2]:
        roadmap.append({
            "topic": topic,
            "priority": "low",
            "reason": "You've mastered the basics! Try medium or hard level problems to push your limits.",
            "suggested_count": 2,
            "difficulty": "medium" if topic_scores[topic].get("avg_score", 0) < 90 else "hard"
        })
        
    return roadmap

async def update_progress_after_attempt(db: AsyncSession, user_id: int, attempt: QuestionAttempt) -> UserProgress:
    progress = await get_or_create_progress(db, user_id)
    
    # 1. Update overall counters
    progress.total_problems_attempted += 1
    if attempt.is_correct:
        progress.total_problems_solved += 1
        
    # 2. Update difficulty distribution
    diff = attempt.difficulty.lower()
    dist = dict(progress.difficulty_distribution or {"easy": 0, "medium": 0, "hard": 0})
    dist[diff] = dist.get(diff, 0) + 1
    progress.difficulty_distribution = dist
    
    # 3. Update topic scores
    scores = dict(progress.topic_scores or {})
    topic = attempt.topic.lower()
    t_stats = scores.get(topic, {"solved": 0, "attempted": 0, "avg_score": 0.0})
    
    t_stats["attempted"] += 1
    if attempt.is_correct:
        t_stats["solved"] += 1
    
    # Recalculate average score
    current_avg = t_stats.get("avg_score", 0.0)
    att_score = attempt.score or (100.0 if attempt.is_correct else 0.0)
    t_stats["avg_score"] = ((current_avg * (t_stats["attempted"] - 1)) + att_score) / t_stats["attempted"]
    
    scores[topic] = t_stats
    progress.topic_scores = scores
    
    # 4. Update strengths, weaknesses, and roadmap
    progress.weak_topics = calculate_weak_topics(scores)
    progress.strong_topics = calculate_strong_topics(scores)
    progress.roadmap = generate_roadmap(scores, progress.weak_topics)
    
    # 5. Update streak & active status
    await update_streak(progress)
    
    progress.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(progress)
    return progress

async def update_streak(progress: UserProgress):
    today = date.today()
    if not progress.last_active:
        progress.current_streak = 1
        progress.longest_streak = 1
    else:
        last_active_date = progress.last_active.date()
        delta = today - last_active_date
        
        if delta.days == 1:
            progress.current_streak += 1
            if progress.current_streak > progress.longest_streak:
                progress.longest_streak = progress.current_streak
        elif delta.days > 1:
            progress.current_streak = 1
            
    progress.last_active = datetime.utcnow()

async def get_dashboard_data(db: AsyncSession, user_id: int) -> Dict[str, Any]:
    progress = await get_or_create_progress(db, user_id)
    
    # Get recent sessions
    sessions_res = await db.execute(
        select(InterviewSession)
        .where(InterviewSession.user_id == user_id)
        .order_by(InterviewSession.started_at.desc())
        .limit(5)
    )
    sessions = sessions_res.scalars().all()
    
    recent_sessions = []
    for s in sessions:
        recent_sessions.append({
            "id": s.id,
            "difficulty": s.difficulty,
            "topics": s.topics,
            "score": s.score or 0.0,
            "total_questions": s.total_questions,
            "correct_answers": s.correct_answers,
            "started_at": s.started_at.isoformat() if s.started_at else None,
            "ended_at": s.ended_at.isoformat() if s.ended_at else None,
            "status": s.status
        })
        
    # Topic breakdown for charts
    topic_breakdown = []
    for topic, stats in (progress.topic_scores or {}).items():
        topic_breakdown.append({
            "subject": topic.replace("_", " ").title(),
            "solved": stats.get("solved", 0),
            "attempted": stats.get("attempted", 0),
            "avg_score": stats.get("avg_score", 0.0)
        })
        
    # Streak details
    streak_data = {
        "current_streak": progress.current_streak,
        "longest_streak": progress.longest_streak,
        "last_active": progress.last_active.isoformat() if progress.last_active else None
    }
    
    return {
        "progress": {
            "total_sessions": progress.total_sessions,
            "total_problems_solved": progress.total_problems_solved,
            "total_problems_attempted": progress.total_problems_attempted,
            "current_streak": progress.current_streak,
            "longest_streak": progress.longest_streak,
            "last_active": progress.last_active,
            "topic_scores": {k: TopicScore(**v) for k, v in (progress.topic_scores or {}).items()},
            "difficulty_distribution": progress.difficulty_distribution or {"easy": 0, "medium": 0, "hard": 0},
            "weak_topics": progress.weak_topics or [],
            "strong_topics": progress.strong_topics or [],
            "roadmap": [RoadmapItem(**r) for r in (progress.roadmap or [])]
        },
        "recent_sessions": recent_sessions,
        "topic_breakdown": topic_breakdown,
        "streak_data": streak_data
    }
