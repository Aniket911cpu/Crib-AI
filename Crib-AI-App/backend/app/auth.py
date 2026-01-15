import os
import firebase_admin
from firebase_admin import credentials, auth, firestore
from fastapi import Header, HTTPException, Depends

# Initialize Firebase Admin
# NOTE: In production, you need a serviceAccountKey.json file.
# For now, we assume standard environment variables or a placeholder check.
try:
    cred = credentials.ApplicationDefault() 
    # Or use: cred = credentials.Certificate('path/to/serviceAccountKey.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
except Exception as e:
    print(f"Warning: Firebase Admin failed to initialize (Expected if no creds provided): {e}")
    db = None

async def verify_token(authorization: str = Header(...)):
    """
    Verifies the Bearer Token from Firebase Auth.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")
    
    token = authorization.split("Bearer ")[1]
    
    try:
        # Verify the token
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        return uid
    except Exception as e:
        print(f"Auth Error: {e}")
        # For dev purposes without real creds, you might bypass:
        # return "dev_user_uid" 
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_user_plan(uid: str = Depends(verify_token)):
    """
    Fetches user plan from Firestore.
    """
    if not db:
        return "free" # Default if DB not connected

    try:
        user_ref = db.collection('users').document(uid)
        doc = user_ref.get()
        if doc.exists:
             return doc.to_dict().get('planType', 'free')
        return 'free'
    except Exception as e:
        print(f"Firestore Error: {e}")
        return 'free'
