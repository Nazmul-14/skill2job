import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(BASE_DIR, "..", "data", "user.json")


# ================= LOAD =================
def load_data():
    if not os.path.exists(FILE):
        return {"users": []}

    with open(FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return {"users": []}


# ================= SAVE =================
def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


# ================= LOGIN =================
def login_user(email, password):
    data = load_data()

    email = email.strip().lower()
    password = password.strip()

    for user in data["users"]:

        u_email = user["email"].strip().lower()
        u_pass = str(user["password"]).strip()

        if u_email == email and u_pass == password:
            return user

    return None


# ================= REGISTER =================
def register_user(name, email, password):
    data = load_data()

    # check duplicate email
    for user in data["users"]:
        if user["email"] == email:
            return None

    # generate new id
    new_id = 1
    if data["users"]:
        new_id = max(u["id"] for u in data["users"]) + 1

    new_user = {
        "id": new_id,
        "name": name,
        "email": email,
        "password": password,
        "skills": [],
        "pathway_step": 0,
        "cv": {}
    }

    data["users"].append(new_user)
    save_data(data)

    return new_user


# ================= GET USER =================
def get_user_by_id(user_id):
    data = load_data()

    for user in data["users"]:
        if user["id"] == user_id:
            return user

    return None


# ================= UPDATE USER =================
def update_user(updated_user):
    data = load_data()

    for i, user in enumerate(data["users"]):
        if user["id"] == updated_user["id"]:
            data["users"][i] = updated_user
            break

    save_data(data)


# ================= SKILLS =================
def add_skill(user_id, skill):
    user = get_user_by_id(user_id)

    if not user:
        return

    if skill not in user["skills"]:
        user["skills"].append(skill)
        update_user(user)


def remove_skill(user_id, skill):
    user = get_user_by_id(user_id)

    if not user:
        return

    if skill in user["skills"]:
        user["skills"].remove(skill)
        update_user(user)


# ================= PATHWAY =================
def get_pathway_step(user_id):
    user = get_user_by_id(user_id)

    if not user:
        return 0

    return user.get("pathway_step", 0)


def update_pathway_step(user_id):
    user = get_user_by_id(user_id)

    if not user:
        return

    user["pathway_step"] = user.get("pathway_step", 0) + 1
    update_user(user)


# ================= CV =================
def get_cv(user_id):
    user = get_user_by_id(user_id)

    if not user:
        return {}

    return user.get("cv", {})


def update_cv(user_id, cv_data):
    user = get_user_by_id(user_id)

    if not user:
        return

    user["cv"] = cv_data
    update_user(user)