from fastapi import APIRouter, Depends, HTTPException, status
from app.models import ProfileUpdate, ProfileDB, TokenData, LevelProgress
from app.auth.utils import get_current_user
from app.db import get_supabase
from supabase import Client
from datetime import datetime

router = APIRouter()

@router.get("/get", response_model=ProfileDB)
async def get_profile(
    current_user: TokenData = Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    profile_data = supabase.table("profiles").select("*").eq("user_id", current_user.user_id).execute()
    
    if not profile_data.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    # Get level progress
    progress_data = supabase.table("level_progress").select("*").eq("user_id", current_user.user_id).execute()
    
    profile = profile_data.data[0]
    profile["progress"] = progress_data.data if progress_data.data else []
    
    return profile

@router.post("/update", response_model=ProfileDB)
async def update_profile(
    profile_update: ProfileUpdate,
    current_user: TokenData = Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    # Check if profile exists
    profile_data = supabase.table("profiles").select("*").eq("user_id", current_user.user_id).execute()
    
    if not profile_data.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    # Update profile
    update_data = profile_update.dict(exclude_unset=True)
    updated_profile = supabase.table("profiles").update(update_data).eq("user_id", current_user.user_id).execute()
    
    if not updated_profile.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile"
        )
    
    # Get level progress
    progress_data = supabase.table("level_progress").select("*").eq("user_id", current_user.user_id).execute()
    
    profile = updated_profile.data[0]
    profile["progress"] = progress_data.data if progress_data.data else []
    
    return profile

@router.post("/update-progress/{level_id}")
async def update_progress(
    level_id: int,
    score: int,
    current_user: TokenData = Depends(get_current_user),
    supabase: Client = Depends(get_supabase)
):
    # Check if level progress exists
    progress_data = supabase.table("level_progress").select("*").eq("user_id", current_user.user_id).eq("level_id", level_id).execute()
    
    now = datetime.utcnow().isoformat()
    
    if progress_data.data:
        # Update existing progress if score is higher
        existing_progress = progress_data.data[0]
        if score > existing_progress["score"]:
            supabase.table("level_progress").update({
                "score": score,
                "completed": True,
                "completed_at": now
            }).eq("id", existing_progress["id"]).execute()
    else:
        # Create new progress
        supabase.table("level_progress").insert({
            "user_id": current_user.user_id,
            "level_id": level_id,
            "score": score,
            "completed": True,
            "completed_at": now
        }).execute()
    
    # Update profile with current level and total score
    profile_data = supabase.table("profiles").select("*").eq("user_id", current_user.user_id).execute()
    profile = profile_data.data[0]
    
    # Get all progress to calculate total score
    all_progress = supabase.table("level_progress").select("*").eq("user_id", current_user.user_id).execute()
    total_score = sum(p["score"] for p in all_progress.data)
    
    # Update current level if completed current one
    current_level = profile["current_level"]
    if level_id == current_level and level_id < 4:  # Assuming 4 levels total
        current_level += 1
    
    supabase.table("profiles").update({
        "current_level": current_level,
        "total_score": total_score
    }).eq("user_id", current_user.user_id).execute()
    
    return {"message": "Progress updated successfully"}

