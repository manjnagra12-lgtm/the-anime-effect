## 👤 About Me & Project Overview

Welcome to my Full-Stack Capstone project! I am an aspiring software engineer currently completing an intensive, AI-Augmented Full-Stack Bootcamp. This platform represents the culmination of my learning, combining a deep passion for the anime community with rigorous software engineering principles.

### 🚀 Project Vision
As an avid fan of animation, I wanted to build more than a static database. **My project is a responsive, full-stack anime platform that bridges content tracking with community engagement.** It serves as a centralized hub where users can seamlessly manage their seasonal watchlists, stay up-to-date with current 2026 releases (like *The Apothecary Diaries* and *Nippon Sangoku*), and share live reactions with other fans via an integrated micro-blogging feed.

### 🛠️ Technical Focus & Learning Objectives
This application was engineered from scratch to demonstrate production-ready proficiency across several core pillars of full-stack development:
* **Agile Planning (LO1.3):** Planned and tracked with an incremental, user-story-driven workflow on the [GitHub Projects board](https://github.com/users/manjnagra12-lgtm/projects/6/views/1). The board links project work to the user stories below; make sure its sharing permissions allow assessors to view it.
* **Robust Backend Architecture (LO1.2/2.1):** Powered by Django's ORM with a custom database schema, strict validation constraints, and relational data integrity.
* **Role-Based Access Control (LO3):** Implements secure, granular permissions differentiating standard users from site administrators to safeguard data modifications.
* **Accessible UX/UI Design (LO1.1):** Built with responsive layouts and accessibility practices such as semantic landmarks, labeled forms, keyboard focus indicators, and contrast improvements. Targeted checks are documented below; this project does not claim a formal audit proving zero WCAG errors.
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

The diagram reflects the current Django models and their foreign-key deletion rules. `ContactMessage` is intentionally independent: visitors can submit a request without creating an account.

```mermaid
erDiagram
    USER ||--o{ BLOGPOST : writes
    USER ||--o{ COMMENT : writes
    BLOGPOST ||--o{ COMMENT : has
    ANIME o|--o{ BLOGPOST : tags
    USER ||--o{ USERTRACKER : tracks
    ANIME ||--o{ USERTRACKER : appears_in
    CONTACTMESSAGE {
        bigint id PK
        varchar name
        varchar email
        varchar subject
        text message
        datetime created_at
        boolean is_read
    }
```


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
title	Varchar(255)	None	Required, indexed
synopsis	Text	None	Optional long-form story overview
total_episodes	PositiveInteger	None	Required, minimum 1; database check constraint
genres	Varchar(255)	None	Optional
studio	Varchar(150)	None	Optional
image	ImageField	None	Optional uploaded image; maximum size 5 MB


3. UserTracker Model (App: tracker)

Acts as a junction table bridging users and shows to handle individual watchlists.

Field Name	Data Type	Key Type	Properties / Constraints
id	Integer	PK	Auto-incrementing, Unique
user_id	Integer	FK	Links to User.id (ON DELETE CASCADE)
anime_id	Integer	FK	Links to Anime.id (ON DELETE CASCADE)
status	Varchar(20)	None	Choices: ['Plan to Watch', 'Watching', 'Completed']
current_episode	PositiveInteger	None	Default: 0 (Validated against Anime.total_episodes)

Composite Constraint: unique constraint on ('user', 'anime')
Prevents a user from adding the same anime to their watchlist more than once.

4. BlogPost Model (App: social)

Feeds the live micro-blogging community space.

Field Name	Data Type	Key Type	Properties / Constraints
id	Integer	PK	Auto-incrementing, Unique
author_id	Integer	FK	Links to User.id (ON DELETE CASCADE)
anime_id	Integer	FK	Links to Anime.id (ON DELETE SET_NULL, Null=True, Blank=True)
content	Text	None	Required; maximum 1,000 characters
created_at	DateTime	None	Auto-populates on creation (orders chronological feed)

5. Comment Model (App: social)

Stores replies on a community post. A comment belongs to one post and one author; deleting either cascades to its comments.

Field Name	Data Type	Key Type	Properties / Constraints
id	Integer	PK	Auto-incrementing, Unique
post_id	Integer	FK	Links to BlogPost.id (ON DELETE CASCADE)
author_id	Integer	FK	Links to User.id (ON DELETE CASCADE)
content	Text	None	Required; maximum 1,000 characters
created_at	DateTime	None	Auto-populates on creation; comments ordered oldest first

6. ContactMessage Model (App: contact)

Stores public requests, including anime suggestions, for staff to review in the Django admin inbox. It has no user foreign key because sign-in is not required.

Field Name	Data Type	Key Type	Properties / Constraints
id	Integer	PK	Auto-incrementing, Unique
name	Varchar(100)	None	Required
email	Varchar(254)	None	Required; validated email address
subject	Varchar(150)	None	Required
message	Text	None	Required; maximum 3,000 characters
created_at	DateTime	None	Auto-populates on creation
is_read	Boolean	None	Default: False; staff can mark the message as read

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

The interface uses a consistent dark palette, visible keyboard focus, a skip link, semantic page landmarks, labeled forms, and responsive CSS Grid/Flexbox layouts. Targeted contrast checks informed control-border and navigation styling improvements. On narrow screens the catalog becomes a single-column list, navigation wraps, and tracker rows stack their progress and actions. On larger desktop displays, the content container expands and the catalog uses a four-column grid while keeping a readable maximum width. Reduced-motion preferences are respected. The catalog and community feed are paginated. Browser checks verified the skip link is keyboard reachable and found no horizontal overflow at 320, 390, 768, and 1,280 CSS pixels. These checks cover selected accessibility and responsive behaviors; they are not a complete WCAG conformance audit or a substitute for assistive-technology testing. The primary user flows are:

The following low-fidelity wireframes document the page structure and responsive intent. They describe layout rather than final visual styling.

**Shared site layout**

```text
DESKTOP
+------------------------------------------------------------------+
| A  The Anime Effect   Discover  Community  About  Contact   Join |
+------------------------------------------------------------------+
|                                                                  |
|                         PAGE CONTENT                             |
|                                                                  |
+------------------------------------------------------------------+
| The Anime Effect     Discover stories...     Instagram YouTube...|
+------------------------------------------------------------------+

MOBILE
+------------------------------+
| A  The Anime Effect    Join  |
| Discover  Community  About   |
| Contact                      |
+------------------------------+
|                              |
|         PAGE CONTENT         |
|                              |
+------------------------------+
| The Anime Effect             |
| Discover stories...          |
|             Instagram YouTube|
|                  X TikTok    |
+------------------------------+
```

**Discover catalog and anime detail**

```text
DISCOVER                              ANIME DETAIL
+--------------------------------+    +--------------------------------+
| Find your next favorite        |    | Discover / Anime title         |
| Explore the catalog...         |    | Anime title                    |
+--------------------------------+    | [Cover]                        |
| Search title, genre... [Search]|    | Episodes · Studio · Genres     |
+--------------------------------+    | Synopsis                       |
| [Anime card] [Anime card]      |    | [Add to my tracker]            |
| [Anime card] [Anime card]      |    +--------------------------------+
|        Previous  Page  Next    |
+--------------------------------+

On narrow screens, catalog cards stack into one column and detail
content stays in a single readable column.
```

**Tracker, community, and contact**

```text
MY TRACKER                           COMMUNITY
+--------------------------------+   +--------------------------------+
| My tracker                    |   | Currently discussing           |
| Anime title · Watching        |   | [Write a post]                 |
| Episode progress   [Update]   |   +--------------------------------+
|                   [Remove]    |   | Author · date · anime tag      |
| Anime title · Plan to Watch   |   | Post text                      |
| Episode progress   [Update]   |   | View comments                  |
+--------------------------------+   +--------------------------------+

CONTACT
+--------------------------------+
| Contact us                     |
| Request or anime suggestion    |
| Name                           |
| Email                          |
| Subject                        |
| Message                        |
| [Send message]                 |
+--------------------------------+
```

```text
Discover → Search/filter catalog → Anime details → Add/update tracker
Community → Read newest posts → Write/edit/delete your own post
Navigation → Register/log in → My tracker → Update or remove an entry
```

The implementation keeps the catalog and social feed public while gating tracker actions and content creation behind authentication. Only staff can manage the catalog, and post edits/deletes are scoped to their author.

The shared header/navigation, page-specific content area, and footer provide a consistent structure. Catalog pages use a search bar followed by a responsive card grid; detail pages place show metadata and synopsis above a single tracker action; tracker pages put each title, status, progress bar, and controls together; community pages use stacked post cards with author/time metadata. The mobile adaptation keeps the same content order, wraps navigation, and stacks cards and tracker actions rather than hiding functionality. During implementation, the catalog and feed were paginated to keep longer manually entered datasets manageable.

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

#### End-to-end browser tests

The optional Playwright suite runs the application on Django's live test server with an isolated test database. It exercises the interface in Chromium and verifies persisted results; the browser is not included in production dependencies.

Install the development dependencies and Chromium once:

```powershell
python -m pip install -r requirements-dev.txt
python -m playwright install chromium
```

Run the browser tests:

```powershell
python manage.py test e2e_tests.browser_flows
```

To also capture the test screenshots used below, set the screenshot directory before running the suite:

```powershell
$env:E2E_SCREENSHOT_DIR = "docs/screenshots/e2e"
python manage.py test e2e_tests.browser_flows
Remove-Item Env:E2E_SCREENSHOT_DIR
```

The four browser tests cover:

- Account registration followed by adding, updating, and removing a tracker entry, including canceling and confirming the removal dialog.
- Publishing a community post, dismissing its success notification, and adding a comment.
- Checking invalid-email browser validation, then submitting a valid contact request and verifying it reaches the admin inbox.
- Keyboard access to the skip link and no horizontal overflow at 320, 390, 768, and 1,280 CSS pixels.

The standard Django suite remains separate at 29 tests; the optional browser suite has four tests and is run explicitly with the command above.

**Latest recorded test run (2 November 2026):** `python manage.py test` — 29 tests passed; `python manage.py test e2e_tests.browser_flows` — 4 Chromium browser tests passed. Django reported no system-check issues.

Screenshots are opt-in and are written to the directory named by `E2E_SCREENSHOT_DIR`. The screenshots shown here were captured from the local test server using the isolated test database; they are illustrative browser-test evidence, not screenshots of the deployed site or evidence of production data.

**Discover page — desktop browser test**

![Discover page during the browser test](docs/screenshots/e2e/01-discover-desktop.png)

**Tracker — mobile browser test**

![Tracker page at mobile width during the browser test](docs/screenshots/e2e/02-tracker-mobile.png)

**Community post and comment**

![Community post and submitted comment during the browser test](docs/screenshots/e2e/03-community-post-and-comment.png)

**Contact request submitted**

![Successful contact request during the browser test](docs/screenshots/e2e/04-contact-request-sent.png)

**Discover page — mobile browser test**

![Discover page at mobile width during the browser test](docs/screenshots/e2e/05-discover-mobile.png)

#### Recorded browser-check results

| Check | Result |
| --- | --- |
| Registration, tracker add/update, and deletion | Passed in Chromium; canceling the confirmation kept the entry, and confirming removed it |
| Community post and comment | Passed in Chromium; the post and comment were visible after submission |
| Success-notification dismissal | Passed in Chromium; dismissing the post-success notification removed it |
| Contact form email validation and submission | Passed in Chromium; an invalid email was rejected by the browser and a valid request was saved |
| Keyboard skip link and responsive layout | Passed in Chromium; the skip link received focus first and no horizontal overflow was found at 320, 390, 768, and 1,280 CSS pixels |
| Django model, view, form, permission, and application tests | 29 tests passed; no Django system-check issues |
| Deployed-site visual review | Discover and Contact screenshots captured at 900 × 700 on 2 November 2026; separate responsive checks found no horizontal overflow at 320, 390, 768, and 1,280 CSS pixels |

The browser suite uses Django's isolated test database; its contact request does not create data in the deployed admin inbox. The Django tests also cover invalid episode progress, content-length validation, ownership restrictions, and missing-cover fallback. A full screen-reader/accessibility audit and a page-by-page keyboard review remain future verification work.

#### Manual browser screenshots

The following desktop screenshots were captured from the deployed site on 2 November 2026 during visual browser checks. The mobile layout was separately checked at 320, 390, 768, and 1,280 CSS-pixel viewport widths; no horizontal page overflow was detected. These desktop images document page appearance only and do not represent successful form submissions or authenticated tracker actions.

**Discover page — desktop viewport (900 × 700)**

![Discover page at desktop viewport](docs/screenshots/discover-desktop.png)

**Contact page — desktop viewport (900 × 700)**

![Contact page with labeled message fields](docs/screenshots/contact-desktop.png)

### Deployment

The application is deployed on Heroku: [The Anime Effect](https://theanimeeffect-72c5f4f763fb.herokuapp.com/). The repository includes a `Procfile` with a Gunicorn web process and a release command that runs database migrations.

#### Deploying to Heroku

1. Create a Heroku app and connect this GitHub repository, or add Heroku as a Git remote. Ensure the app uses the Python buildpack; Heroku installs the pinned packages from `requirements.txt`.
2. Attach a Heroku-compatible PostgreSQL database. The database add-on supplies `DATABASE_URL`; production settings reject SQLite and require PostgreSQL.
3. Configure the app's environment variables in Heroku **Settings → Config Vars**. Example values for this app:

   | Variable | Example value |
   | --- | --- |
   | `DJANGO_SECRET_KEY` | A newly generated, private random value |
   | `DJANGO_DEBUG` | `False` |
   | `DJANGO_ALLOWED_HOSTS` | `theanimeeffect-72c5f4f763fb.herokuapp.com` |
   | `CSRF_TRUSTED_ORIGINS` | `https://theanimeeffect-72c5f4f763fb.herokuapp.com` |
   | `DJANGO_SECURE_COOKIES` | `True` |
   | `DJANGO_SECURE_SSL_REDIRECT` | `True` |
   | `DATABASE_URL` | Supplied by the attached PostgreSQL add-on |

   Keep the secret key private and set it only in the hosting provider's config. Enable HSTS only after confirming HTTPS works correctly for the deployed domain.
   Generate a fresh key locally with `python -c "import secrets; print(secrets.token_urlsafe(64))"` and paste it into the Heroku config; do not save it in the repository.
4. Deploy the `main` branch from the Heroku-connected GitHub repository, or push it through the Heroku Git remote:

   ```powershell
   git push heroku main
   ```

   The `release` process in `Procfile` runs `python manage.py migrate` before the new release serves traffic.
5. Review the release and application logs, then run Django's deployment checks:

   ```powershell
   $app = "your-heroku-app-name"
   heroku logs --num 100 --app $app
   heroku run python manage.py check --deploy --app $app
   ```

   Address any deployment-check warnings that apply to the hosting setup. Open the deployed URL and smoke-test registration, login, the catalog, tracker, community, and contact form. Do not submit a real contact request unless you intend to add it to the live admin inbox.

For assessment, confirm the Heroku Config Vars match the secure production values above and that the deployment-check command completes without unresolved security warnings. The source defaults `DJANGO_DEBUG` to `False` in production and refuses to start without a non-placeholder secret key and a production PostgreSQL URL; runtime config values must still be verified in Heroku.

### AI-assisted development reflection

I used GitHub Copilot throughout development to help shape the Django app structure and turn the project goals into features such as the anime catalog, private watch tracker, and community feed. I reviewed suggestions against the user stories and adapted them to the app rather than accepting generated code without checking it.

Copilot also helped me investigate errors during development, including critical issues that led me to restart early iterations. Working through the failures with its help made it easier to identify likely causes and continue building toward a stable result.

For user experience, I used Copilot to explore responsive layout and accessibility improvements. This included addressing narrow-screen overflow, improving focus and control styling, and keeping catalog and community lists manageable through pagination. These changes were checked with responsive browser tests and targeted keyboard and contrast checks; they do not establish formal WCAG conformance.

Copilot supported drafting and extending tests for account flows, permissions, catalog management, tracker validation, community posts/comments, and contact submissions. I reviewed the test expectations against the application behavior, ran the Django and Chromium suites, and adjusted tests when browser or database behavior exposed gaps. The recorded result is 29 passing Django tests and 4 passing browser tests. Using AI shortened troubleshooting and test iteration, while running the tests and reviewing the behavior helped me stay responsible for the final implementation.

### Considerations for next updates

- **Improve contact request handling:** Add optional email notifications for staff and an acknowledgement for the sender. Add rate limiting or spam protection before enabling email delivery.
- **Add community moderation tools:** Let staff review or remove inappropriate posts and comments, and give users a way to report content.
- **Expand account support:** Add password-reset and email-verification flows, with clear guidance for users who lose access to their account.
- **Strengthen accessibility verification:** Continue page-by-page keyboard and screen-reader testing, check text and control contrast, and add automated accessibility checks to the development workflow.
- **Expand end-to-end coverage:** Add browser checks for invalid form submissions, logged-out restrictions, and other accessibility interactions as the application evolves.
- **Use durable production media storage:** Store uploaded anime covers in persistent object storage so they remain available across deployments and dyno restarts.
