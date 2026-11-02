## 👤 About Me & Project Overview

Welcome to my Full-Stack Capstone project! I am an aspiring software engineer currently completing an intensive, AI-Augmented Full-Stack Bootcamp. This platform represents the culmination of my learning, combining a deep passion for the anime community with rigorous software engineering principles.

### 🚀 Project Vision
As an avid fan of animation, I wanted to build more than a static database. **My project is a responsive, full-stack anime platform that bridges content tracking with community engagement.** It serves as a centralized hub where users can seamlessly manage their seasonal watchlists, stay up-to-date with current 2026 releases (like *The Apothecary Diaries* and *Nippon Sangoku*), and share live reactions with other fans via an integrated micro-blogging feed.

### 🛠️ Technical Focus & Learning Objectives
This application was engineered from scratch to demonstrate production-ready proficiency across several core pillars of full-stack development:
* **Agile Planning (LO1.3):** Built using an incremental, user-story-driven workflow to track milestones and deliverables.
* **Robust Backend Architecture (LO1.2/2.1):** Powered by Django's ORM with a custom database schema, strict validation constraints, and relational data integrity.
* **Role-Based Access Control (LO3):** Implements secure, granular permissions differentiating standard users from site administrators to safeguard data modifications.
* **Accessible UX/UI Design (LO1.1):** Styled with modern CSS/Bootstrap frameworks to ensure a fully mobile-responsive interface that meets WCAG accessibility guidelines.
* Static templates for reuse and to keep a consistant theme

## User case stories

User Story 1: User Registration

• As a visitor,
I want to create an account with a unique username, email, and password,
So that I can access the tracking and blogging features of the site.
• Acceptance Criteria:
	• Registration form includes field validation (e.g., matching passwords, valid email format).
	• Front-end form clearly labels required fields and displays helpful error messages for invalid input.
	• Successfully registered users are automatically logged in and redirected to the home/dashboard page.

User Story 2: Role-Based Login & State Reflection

• As a registered user,
I want to securely log into my account,
So that I can view my personalized dashboard and navigation options.
• Acceptance Criteria:
	• Nav bar dynamically switches based on login state ({% if user.is_authenticated %}).
	• Logged-in users see their username, a link to "My Tracker", and a "Logout" button. Anonymous visitors see "Login" and "Register".
	• Invalid login attempts display a clear, accessible error message without revealing sensitive security details.

User Story 3: Restricted Access Control

• As a site owner,
I want to restrict tracking and social actions to authorized roles only,
So that anonymous users cannot manipulate data or post spam.
• Acceptance Criteria:
	• Unauthenticated users trying to access /tracker/ or /blog/create/ are redirected to the login page (using Django's @login_required or Mixins).
	• Regular users attempting to access admin routes (like adding an anime to the global directory) receive a HTTP 403 Forbidden error or a redirection with an error message.

📖 Epic 2: Anime Information & Directory (LO1 / LO2)


User Story 4: Browse & Search Anime Database

• As a user (logged in or out),
As a visitor,
I want to view a clean, responsive grid list of anime and click into them for details,
So that I can read synopses, genres, and studio information.
• Acceptance Criteria:
	• The anime catalog layout uses semantic HTML and adapts fluidly across mobile, tablet, and desktop screens (Flexbox/Grid/Bootstrap).
	• Text and background choices meet WCAG contrast requirements.
	• Clicking an anime card takes the user to a detailed view showing all information stored in the Anime database model.

User Story 5: Admin Content Management

• As an Admin,
I want to create, update, and delete anime entries from the global database via the front-end or admin panel,
So that the site's catalog remains accurate and up to date.
• Acceptance Criteria:
	• Only users with is_staff or is_superuser privileges can access the creation/editing forms.
	• Database changes scale cleanly via standard Django migrations.

📊 Epic 3: Personal Watchlist Tracking (LO2)


User Story 6: Add & Update Tracked Anime (Create & Update)

• As a logged-in user,
I want to add an anime to my tracking list, select my watch status, and update my episode progress,
So that I can keep an organized log of my viewing history.
• Acceptance Criteria:
	• Users can add an anime from its detail page using a form with a dropdown for status (Plan to Watch, Watching, Completed).
	• Form validation restricts the user from setting an episode number lower than 0 or higher than the total episode count of the anime.
	• Saving changes updates the record securely using Django's ORM.

User Story 7: View & Manage Watchlist (Read & Delete)

• As a logged-in user,
I want to view a dedicated "My Tracker" dashboard and remove items if I choose,
So that I can review my historical data or clean up accidental entries.
• Acceptance Criteria:
	• "My Tracker" displays a comprehensive list of only the current user's tracked items.
	• A "Remove" button triggers a secure deletion of that specific tracker instance from the database.
	• Triggering a deletion displays a dismissible Django success message ("Anime successfully removed from your list").

💬 Epic 4: Social Blog & Feed (LO2)


User Story 8: Publish a Blog Post (Create)

• As a logged-in user,
I want to write and publish a blog post (with an optional tag for a specific anime),
So that I can share my thoughts with the wider community.
• Acceptance Criteria:
	• The creation form includes validation preventing empty submissions or text that exceeds character limits.
	• Successfully publishing a post triggers a visual success message notification for the user.

User Story 9: View the Live Community Blog Feed (Read)

• As a user,
I want to view a reverse-chronological feed of all community blog posts,
So that I can see the latest discussions and reactions seamlessly.
• Acceptance Criteria:
	• The feed loads posts dynamically from the database, displaying the author's name, timestamp, content, and linked anime (if applicable).
	• The layout behaves responsively and renders content conditionally depending on whether the post author is the active logged-in user.

User Story 10: Edit & Delete Personal Posts (Update & Delete)

• As a post author,
I want to modify or permanently remove a blog post I wrote,
So that I can fix typos or retract my commentary.
• Acceptance Criteria:
	• "Edit" and "Delete" actions are structurally hidden from anyone who is not the creator of that specific post.
	• Back-end logic verifies user ownership before completing any POST/DELETE operations to secure data records.



## ERD

*Database Relations Map

  ┌──────────────┐              ┌─────────────────┐
  │     USER     │ 1 ──────── * │    BLOGPOST     │
  └──────────────┘              └─────────────────┘
         │ 1                             * │ (Optional)
         │                                 │
         │ *                               │ 1
  ┌──────────────┐              ┌─────────────────┐
  │ USERTRACKER  │ * ──────── 1 │      ANIME      │
  └──────────────┘              └─────────────────┘


🗂️ Detailed Schema Architecture


1. User Model (django.contrib.auth.models.User)

This is Django’s built-in authentication model, handling account registration and system access rules.

Field Name	Data Type	Key Type	Properties / Constraints
id	Integer	PK	Auto-incrementing, Unique
username	Varchar(150)	Unique	Required, unique login credential
email	Varchar(254)	None	Validated email string
is_staff	Boolean	None	Default: False (Controls Admin panel access)


2. Anime Model (App: catalog)

Stores general descriptive data for the site directory. Controlled exclusively by Admin roles.

Field Name	Data Type	Key Type	Properties / Constraints
id	Integer	PK	Auto-incrementing, Unique
title	Varchar(255)	None	Required, indexable name
synopsis	Text	None	Long-form story overview
total_episodes	PositiveInteger	None	Must be > 0 (Used to validate tracker caps)


3. UserTracker Model (App: tracker)

Acts as a junction table bridging users and shows to handle individual watchlists.

Field Name	Data Type	Key Type	Properties / Constraints
id	Integer	PK	Auto-incrementing, Unique
user_id	Integer	FK	Links to User.id (ON DELETE CASCADE)
anime_id	Integer	FK	Links to Anime.id (ON DELETE CASCADE)
status	Varchar(20)	None	Choices: ['Plan to Watch', 'Watching', 'Completed']
current_episode	PositiveInteger	None	Default: 0 (Validated against Anime.total_episodes)

Composite Constraint: unique_together = ('user', 'anime')
Prevents a user from adding the same anime to their watchlist more than once.

4. BlogPost Model (App: social)

Feeds the live micro-blogging community space.

Field Name	Data Type	Key Type	Properties / Constraints
id	Integer	PK	Auto-incrementing, Unique
author_id	Integer	FK	Links to User.id (ON DELETE CASCADE)
anime_id	Integer	FK	Links to Anime.id (ON DELETE SET_NULL, Null=True, Blank=True)
content	Text	None	Character limit validation applies
created_at	DateTime	None	Auto-populates on creation (orders chronological feed)

## Running the project locally

The project uses Django with SQLite by default, so the database starts empty and you can enter your own records while testing. No sample accounts, anime, or posts are loaded automatically.

1. Create and activate a virtual environment, then install the pinned packages:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```

2. Create your local, ignored environment file from the safe example:

   ```powershell
   Copy-Item .env.example .env
   ```

   `.env` is ignored by Git. The example contains only a development placeholder; replace it with a private key if you need one locally. Never put production secrets or real API credentials in `.env.example`.

3. Create the local database tables and an administrator account:

   ```powershell
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. Start the development server and open `http://127.0.0.1:8000/`:

   ```powershell
   python manage.py runserver
   ```

Use `/admin/` to add anime records. Staff accounts can also add, edit, and delete catalog entries in the site UI. Public account registration is available from the navigation; registered users can maintain their own tracker and publish posts.

Staff can choose an optional cover image when adding or editing an anime. Images are validated as actual image files and limited to 5 MB; uploaded covers appear on the Explore anime cards and anime detail pages. Local uploads are stored under `media/` (ignored by Git). In production, configure persistent or object storage for media and serve it through the hosting platform; Django's development media route is enabled only with `DJANGO_DEBUG=True`.

## How to use the site

### First-time setup: add anime (staff)

The local database starts empty, so add a few catalog entries before trying the watchlist or tagging a post with an anime.

1. Sign in with the superuser account created during setup at `/accounts/login/`.
2. From the navigation, open **Admin**, or visit `/admin/` directly.
3. In the Django admin, open **Anime** and select **Add anime**. Alternatively, use **Add anime** on the Discover page.
4. Enter a title and total episode count. Add a synopsis, genres, and studio if available.
5. Optionally select a cover image. Keep the image at or below 5 MB and use a supported image format such as JPEG, PNG, GIF, or WebP.
6. Save the entry. It will appear in **Explore anime**; select its card to see the detail page.
7. To make changes later, open the anime and choose **Edit**. Staff can also delete an entry; deleting anime removes its tracker entries, while related blog posts remain and lose their anime link.

### Create an account and explore

1. Select **Join** in the navigation and enter a username, email address, and password. Email addresses must be unique.
2. Successful registration signs you in automatically. To return later, use **Log in** with your username and password.
3. On **Discover**, browse the anime cards or search by title, synopsis, genre, or studio. Use the page controls to move through a longer catalog.
4. Select an anime card to open its details, including the synopsis, episode count, studio, genres, and cover image when one is available.

### Manage your watchlist

1. While signed in, select **Add to my tracker** on an anime detail page.
2. Choose **Plan to Watch**, **Watching**, or **Completed**, then enter your current episode. Progress must be from 0 through that anime's total episode count.
3. Save to see the entry on **My tracker**. Each row shows its status and episode progress.
4. Select **Update** to change the status or episode count. Select **Remove** to remove the entry; confirm the browser prompt to proceed. Your tracker entries are private to your account.

### Read and write community posts

1. Open **Community** to read the newest posts. Posts may include a link to a related anime.
2. To post, sign in and choose **Write a post** (or **Join the conversation** if signed out).
3. Write up to 1,000 characters and optionally choose an anime to tag. Select **Publish post**.
4. Your own posts show **Edit** and **Delete** controls. Only the author can change or remove their post; deletion requires confirmation.
5. Use the feed's page controls to browse older posts.

### Sign out

Select **Log out** in the navigation when finished. You can sign in again at any time; your account's watchlist and posts remain saved.

### Environment configuration

The app loads `.env` for local development and reads deployment values from environment variables. Existing environment variables take precedence over values in `.env`.

| Variable | Purpose | Default |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` or `SECRET_KEY` | Django signing key; required when debug is off and must be private | No production default |
| `DJANGO_DEBUG` | Enables Django debug mode when set to `true`, `1`, or `yes` | `False` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated hostnames | `localhost,127.0.0.1` |
| `CSRF_TRUSTED_ORIGINS` | Comma-separated trusted HTTPS origins; entries are normalized without trailing slashes | Heroku and Code Institute HTTPS subdomains |
| `DJANGO_SECURE_COOKIES` | Marks session and CSRF cookies as HTTPS-only | `False` |
| `DJANGO_SECURE_SSL_REDIRECT` | Redirects HTTP requests to HTTPS (enable only behind a TLS-terminating proxy) | `False` |
| `DJANGO_SECURE_HSTS_SECONDS` | HSTS duration in seconds; enable only after HTTPS is confirmed | `0` |
| `DATABASE_URL` | PostgreSQL connection URL; required in production. PostgreSQL connections use SSL. | Local `db.sqlite3` |

Never commit `.env`, production credentials, or a production secret key. `.gitignore` excludes `.env`, `.env.*`, key files, and the `secrets/` directory; `.env.example` is the only environment-file exception and must contain placeholders only. Django refuses to start in production mode without `DJANGO_SECRET_KEY` or when the example placeholder is used. Set production secrets directly in the hosting provider's secret/environment settings, not in source files or browser JavaScript. If the application later uses an external API, read its key on the server from an environment variable (for example `os.environ["ANIME_PROVIDER_API_KEY"]`) and never render it into a template or static asset. Set `DJANGO_DEBUG=False`, configure the deployed hostname in `DJANGO_ALLOWED_HOSTS`, and enable secure cookies/HTTPS redirect/HSTS only when the host is serving HTTPS through a trusted TLS-terminating proxy.

### UX and responsive design

The interface uses a consistent dark palette with high-contrast text, visible keyboard focus, a skip link, semantic page landmarks, labeled forms, and responsive CSS Grid/Flexbox layouts. On narrow screens the catalog becomes a single-column list, navigation wraps, and tracker rows stack their progress and actions. On larger desktop displays, the content container expands and the catalog uses a four-column grid while keeping a readable maximum width. Reduced-motion preferences are respected. The catalog and community feed are paginated. The primary user flows are:

```text
Discover → Search/filter catalog → Anime details → Add/update tracker
Community → Read newest posts → Write/edit/delete your own post
Navigation → Register/log in → My tracker → Update or remove an entry
```

The implementation keeps the catalog and social feed public while gating tracker actions and content creation behind authentication. Only staff can manage the catalog, and post edits/deletes are scoped to their author.

The initial wireframe was a shared header/navigation above a page-specific content area and footer. Catalog pages use a search bar followed by a responsive card grid; detail pages place show metadata and synopsis above a single tracker action; tracker pages put each title, status, progress bar, and controls together; community pages use stacked post cards with author/time metadata. The mobile adaptation keeps the same content order, wraps navigation, and stacks cards and tracker actions rather than hiding functionality. During implementation, the catalog and feed were paginated to keep longer manually entered datasets manageable.

### Tests

Run the automated test suite with:

```powershell
python manage.py test
```

The current automated suite contains **29 Django tests**, verified with:

```text
Ran 29 tests
OK
System check identified no issues
```

Coverage includes:

- Account registration, login/logout, and duplicate email validation.
- Catalog search and detail pages, staff-only anime create/edit/delete, cover uploads, and fallback to a bundled cover when an uploaded image is unavailable.
- Tracker privacy, status/progress validation, and episode limits.
- Community feed and post details, authenticated comment creation, comment length validation, post creation and length validation, and author-only post editing/deletion.
- Contact form rendering, submission and validation, and staff access to the admin inbox.
- About page content and shared social media links.

The test suite verifies application behavior; it does not replace manual browser checks for accessibility and responsive behavior.

Manual browser checks (including the small JavaScript interactions):

| Check | Expected result |
| --- | --- |
| Resize the catalog, detail, tracker, feed, About, and Contact pages from 320 px mobile width through tablet, desktop, and ultrawide widths | No horizontal overflow; content and controls remain available, with more catalog columns on wide displays |
| Use Tab/Shift+Tab and Enter from the top of each page | Focus indicator is visible and links/forms remain usable |
| Dismiss a success notification | The selected notification disappears |
| Submit a tracker removal, then cancel the confirmation | The entry remains; confirming removes only the signed-in user's entry |
| Try an invalid episode count, an overlong post, and an invalid contact email | The form stays open and displays a field-specific validation message |
| Open another user's post edit/delete URL | The request is denied (404) and the post remains unchanged |
| Open the catalog when a saved cover image is unavailable | A matching bundled static cover is used, or a title placeholder is shown |

These are repeatable checks for manual use; automated Django test results are listed above.

### Deployment

The repository includes a `Procfile` for a WSGI host. Its Heroku `release` process runs `python manage.py migrate` on each deploy, and its `web` process starts Gunicorn. Configure `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `DJANGO_SECURE_COOKIES=True`, `DJANGO_SECURE_SSL_REDIRECT=True`, `DJANGO_SECURE_HSTS_SECONDS` (after HTTPS is verified), and a persistent PostgreSQL `DATABASE_URL` in the host's environment; do not use the local SQLite file as production storage. PostgreSQL connections are configured to require SSL, including Neon. During Heroku's build, `collectstatic` can run before runtime config vars are available, so settings allow that command alone to use a temporary build-only key and SQLite database. This build-only configuration is not used by the web or release processes; the app still requires a production secret and database at runtime. The release process applies migrations:

```sh
python -m pip install -r requirements.txt
python manage.py collectstatic --noinput
```

Start the web service with `gunicorn config.wsgi:application` (also defined in `Procfile`). Create a staff user with `python manage.py createsuperuser`, then enter catalog data through `/admin/`. Before launch, confirm debug mode is off, the production host is allowed, HTTPS is enabled by the platform, and the deployed catalog/authentication/tracker/blog flows work end to end.

#### Heroku configuration

Heroku does not read the repository's local `.env` file. Add config vars in **Heroku Dashboard → Settings → Config Vars** (or with `heroku config:set`):

- `DJANGO_SECRET_KEY`: a newly generated, private Django secret. Settings also accept Heroku's conventional `SECRET_KEY` name.
- `DJANGO_ALLOWED_HOSTS`: your app hostname, for example `your-app-name.herokuapp.com` (add any custom hostname as a comma-separated value).
- `CSRF_TRUSTED_ORIGINS`: trusted HTTPS origins, for example `https://your-app-name.herokuapp.com` (add any custom domain's HTTPS origin as another comma-separated value; do not add trailing slashes).
- `DJANGO_DEBUG`: `False`.
- `DATABASE_URL`: set the PostgreSQL connection string from Neon or another managed PostgreSQL provider. Keep the URL private; it contains the database credentials. Production settings require PostgreSQL and connect with SSL. Do not rely on the dyno's local SQLite file.
- Once HTTPS is confirmed, set `DJANGO_SECURE_COOKIES=True` and `DJANGO_SECURE_SSL_REDIRECT=True`. Enable HSTS only after verifying the site works over HTTPS.

Create a managed PostgreSQL database (such as Neon), then put its connection URL in Heroku **Settings → Config Vars** as `DATABASE_URL`. Do not paste the connection URL into source code or commit it. The app parses this URL, requires SSL for PostgreSQL, and runs migrations in the Heroku release phase. Generate a secret locally without putting it in the repository, then set it on the app:

```powershell
$secret = python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
heroku config:set "DJANGO_SECRET_KEY=$secret" "DJANGO_DEBUG=False" "DJANGO_ALLOWED_HOSTS=your-app-name.herokuapp.com" --app your-app-name
```

Replace both example app names with your actual Heroku app name. Then redeploy. The build runs `collectstatic`; the `Procfile` starts Gunicorn. If collection still fails, inspect the full build log above Heroku's generic collectstatic message—the underlying traceback is needed to diagnose a different failure. Do not disable static collection as a workaround because the app's styles and JavaScript are served as static assets.

### AI-assisted development reflection

Copilot assisted with the Django project structure, feature implementation, and tests. The generated work was adapted to this project's model relationships and ownership rules, and validation tests were added for episode caps, post length, and duplicate registration email. Running the test suite exposed implementation issues early and provided a repeatable check of the main user flows. Shared templates and a small set of responsive styles keep the experience consistent without introducing a frontend framework.
