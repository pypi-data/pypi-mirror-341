## 📦  Import‑to‑Usage Cheat‑Sheet

Think of the import block as a toolbox: once a name is imported, you can grab it anywhere below that point in the file.  
This table shows exactly which “tool” is used where in **`app.py`**.

| Import | Purpose | Where it’s used in `app.py` |
|--------|---------|-----------------------------|
| **Flask** | Create the web‑app object | `app = Flask(__name__)` |
| **render_template** | Render Jinja2 templates | `home`, `login`, `register`, `services`, `contact_form`, `private_videos` |
| **request** | Access form data & headers | `login()`, `register()`, `contact_form()` |
| **redirect** / **url_for** | Navigate between routes | After login/logout/register; after contact‑form submit |
| **session** | Signed cookie for per‑user data | `home()` (`if 'username' in session:`) |
| **flash** | One‑shot success/error messages | `register()`, `contact_form()`, `logout()` |
| **jsonify** | Return JSON API responses | `login()` (`return jsonify({...})`) |
| **MongoClient** | Connect to MongoDB Atlas | `client = MongoClient(decoded_mongo_url)` → all DB calls |
| **generate_password_hash** / **check_password_hash** | Secure password hashing & verification | Hash in `register()`, verify in `login()` |
| **quote_plus** | URL‑encode credentials in the Mongo URI | Building `decoded_mongo_url` |
| **ObjectId** | Convert string → MongoDB primary key | `User.get()` (`ObjectId(user_id)`) |
| **os** | Env‑vars & file‑paths (future‑proof) | e.g. `os.getenv()`—not shown yet but reserved |
| **LoginManager** | Central auth manager | `login_manager = LoginManager()` & `login_manager.init_app(app)` |
| **login_user** | Log a user in | Inside `login()` |
| **login_required** | Protect private routes | Decorator on `/logout` (and optionally `/videos`) |
| **logout_user** | Log a user out | `logout()` |
| **current_user** | Proxy to the logged‑in user | Checks in `login()`, `/videos`, `/logout` |
| **UserMixin** | Adds default methods to `User` class | Inherits inside your `User` model |
| **SECRET_KEY** | Signs sessions & CSRF tokens | `app.secret_key = SECRET_KEY` |
| **MONGO_USERNAME / MONGO_PASSWORD** | Credentials for MongoDB | Interpolated into `decoded_mongo_url` |

| **MONGO_URI** | (Optional) pre‑built connection string | *Not used* in this file, but kept for flexibility |

| **EMAIL_USER** | “From” address for outgoing mail | Passed to `send_email()` in `contact_form()` |

| **send_email** | Helper that sends email via SMTP/API | Two calls in `contact_form()` |

| **get_videos** | Fetches private‑video metadata | Used in `private_videos()` |

> **Tip:** Linters like *flake8* will warn you if an import never gets referenced (`F401 unused import`). That’s an easy way to keep the toolbox clean.
