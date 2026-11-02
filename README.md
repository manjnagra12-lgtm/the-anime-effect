## 👤 About Me & Project Overview

Welcome to my Full-Stack Capstone project! I am an aspiring software engineer currently completing an intensive, AI-Augmented Full-Stack Bootcamp. This platform represents the culmination of my learning, combining a deep passion for the anime community with rigorous software engineering principles.

### 🚀 Project Vision
As an avid fan of animation, I wanted to build more than a static database. **My project is a responsive, full-stack anime platform that bridges content tracking with community engagement.** It serves as a centralized hub where users can seamlessly manage their seasonal watchlists, stay up-to-date with current 2026 releases (like *The Apothecary Diaries* and *Nippon Sangoku*), and share live reactions with other fans via an integrated micro-blogging feed.

### 🛠️ Technical Focus & Learning Objectives
This application was engineered from scratch to demonstrate production-ready proficiency across several core pillars of full-stack development:
* **Agile Planning (LO1.3):** Built using an incremental, user-story-driven workflow. The [GitHub Projects board](https://github.com/users/manjnagra12-lgtm/projects/6) currently shows all 10 user stories in Done, with none in Backlog, Ready, In progress, or In review (checked 2 November 2026).
* **Robust Backend Architecture (LO1.2/2.1):** Powered by Django's ORM with a custom database schema, strict validation constraints, and relational data integrity.
* **Role-Based Access Control (LO3):** Implements secure, granular permissions differentiating standard users from site administrators to safeguard data modifications.
* **Accessibility-focused UX/UI Design (LO1.1):** Uses semantic templates, visible keyboard focus, labeled forms, and responsive CSS; accessibility checks and remaining limitations are documented below.
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

Staff can choose an optional cover image when adding or editing an anime. Images are validated as actual image files and limited to 5 MB; uploaded covers appear on the Explore anime cards and anime detail pages. Local uploads are stored under `media/` (ignored by Git). For a bundled fallback cover, keep the file in `static/images/` with the same basename as the catalog record's image filename; Django uses that static asset if the uploaded media file is missing. In production, configure persistent or object storage for uploaded media and serve it through the hosting platform; Django's development media route is enabled only with `DJANGO_DEBUG=True`.

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
| `DATABASE_URL` | PostgreSQL connection URL; required in production. PostgreSQL connections use SSL. | Local `db.sqlite3` |

Never commit `.env`, production credentials, or a production secret key. `.gitignore` excludes `.env`, `.env.*`, key files, and the `secrets/` directory; `.env.example` is the only environment-file exception and must contain placeholders only. Django refuses to start in production mode without `DJANGO_SECRET_KEY` or when the example placeholder is used. Set production secrets directly in the hosting provider's secret/environment settings, not in source files or browser JavaScript. If the application later uses an external API, read its key on the server from an environment variable (for example `os.environ["ANIME_PROVIDER_API_KEY"]`) and never render it into a template or static asset.

When `DJANGO_DEBUG=False`, Django enforces HTTPS redirects, secure session and CSRF cookies, and one-year HSTS for the app hostname and its subdomains. HSTS preloading is not enabled. Heroku terminates TLS before forwarding requests to Django; `SECURE_PROXY_SSL_HEADER` trusts Heroku's `X-Forwarded-Proto` header so HTTPS requests are not redirected repeatedly. These production settings are intentionally not controlled by optional environment flags. Keep the Heroku app on HTTPS and set `DJANGO_DEBUG=False`, `DJANGO_ALLOWED_HOSTS` to its hostname (without a scheme), `CSRF_TRUSTED_ORIGINS` to its HTTPS origin, and `DATABASE_URL` to its PostgreSQL database.

### UX and responsive design

The interface uses a consistent dark palette, visible keyboard focus, a skip link, semantic page landmarks, labeled forms, and responsive CSS Grid/Flexbox layouts. On narrow screens the catalog becomes a single-column list, navigation wraps, and tracker rows stack their progress and actions. On larger desktop displays, the content container expands and the catalog uses a four-column grid while keeping a readable maximum width. Reduced-motion preferences are respected. The catalog and community feed are paginated. Accessibility checks and known limits are documented in the [accessibility audit](docs/accessibility-audit.md); this review is not a certification of full WCAG conformance. The primary user flows are:

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

#### Accessibility audit

The [accessibility audit report](docs/accessibility-audit.md) records the automated scan, keyboard and form checks, contrast measurements, and areas that still need assistive-technology testing. On 2 November 2026, axe-core 4.10.3 reported zero violations for WCAG 2.0/2.1 A and AA rules across seven representative public pages in local Chromium. This is useful evidence, not proof that every criterion or authenticated state conforms.

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

- Account registration followed by adding, updating, and removing a tracker entry; cancelling the removal keeps the entry.
- Publishing a community post, dismissing its success notification, and adding a comment.
- Checking invalid-email browser validation, then submitting a valid contact request and verifying it reaches the admin inbox.
- Keyboard access to the skip link and horizontal-overflow checks on seven public page types at 320, 390, 768, and 1,280 CSS-pixel viewport widths. The signed-in tracker and post-detail/comment flows are also checked at those widths.

The standard Django suite remains separate at 29 tests; the optional browser suite has four tests and is run explicitly with the command above.

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

Recorded browser-check results (including JavaScript interactions):

| Check | Result |
| --- | --- |
| Resize Discover, anime detail, About, Contact, Community, Log in, and Register pages to 320, 390, 768, and 1,280 CSS-pixel viewport widths | **Pass** — no document-level horizontal overflow in the Playwright browser checks |
| Resize the signed-in tracker and post-detail/comment flow to the same viewport widths | **Pass** — no document-level horizontal overflow in the Playwright browser checks |
| Press Tab from the top of Discover | **Pass** — focus reaches the skip link, which targets `#main-content` |
| Dismiss tracker and post-publication success notifications | **Pass** — the selected notification is removed from the page |
| Cancel and then confirm tracker removal | **Pass** — cancelling leaves the entry visible; confirming removes it |
| Submit an invalid contact email, then a valid request | **Pass** — browser email validation blocks the invalid value; the valid request is saved to the admin inbox |
| Validate episode limits, post length, and author-only editing/deletion | **Pass** — covered by the standard Django test suite; these checks are not represented as browser tests |
| Exercise normal form labels and automated accessibility rules on the seven audited public page types | **Pass with limitations** — see the [accessibility audit](docs/accessibility-audit.md) for axe results and incomplete checks |

These are recorded automated browser and Django test outcomes, not a claim that every interaction has been manually tested. Screen-reader operation and 200% browser zoom/text resizing remain outstanding manual checks; responsive viewport measurements do not substitute for either.

#### Manual browser screenshots

The following desktop screenshots were captured from the deployed site on 2 November 2026 during visual browser checks. The mobile layout was separately checked at 320, 390, 768, and 1,280 CSS-pixel viewport widths; no horizontal page overflow was detected. These desktop images document page appearance only and do not represent successful form submissions or authenticated tracker actions.

**Discover page — desktop viewport (900 × 700)**

![Discover page at desktop viewport](docs/screenshots/discover-desktop.png)

**Contact page — desktop viewport (900 × 700)**

![Contact page with labeled message fields](docs/screenshots/contact-desktop.png)

### Deployment

The production site is hosted on Heroku. These steps deploy the current Git branch through the Heroku Git CLI. Heroku's release phase in `Procfile` runs migrations before the new web release starts.

1. Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli), sign in with `heroku login`, and set the app name in PowerShell:

   ```powershell
   $appName = "your-heroku-app-name"
   $appHost = "$appName.herokuapp.com"
   ```

   Confirm the app has a PostgreSQL database attached. The app requires `DATABASE_URL` and refuses to start in production without it. If no database is attached, select a suitable Heroku Postgres plan and create it with `heroku addons:create heroku-postgresql:essential-0 --app $appName`; check the plan and billing before creating an add-on.
2. Configure the non-secret environment values:

   ```powershell
   heroku config:set DJANGO_DEBUG=False "DJANGO_ALLOWED_HOSTS=$appHost" "CSRF_TRUSTED_ORIGINS=https://$appHost" --app $appName
   ```

   If the app uses a custom domain, include that hostname in `DJANGO_ALLOWED_HOSTS` and its `https://` origin in `CSRF_TRUSTED_ORIGINS`.
3. Generate and set a private signing key. Do not put its value in the repository or README:

   ```powershell
   $secret = python -c "import secrets; print(secrets.token_urlsafe(64))"
   heroku config:set "DJANGO_SECRET_KEY=$secret" --app $appName
   Remove-Variable secret
   ```

4. Ensure the Heroku Git remote is configured, then deploy the current branch:

   ```powershell
   heroku git:remote --app $appName
   git push heroku HEAD:main
   ```

5. Verify the release and production settings:

   ```powershell
   heroku config:get DJANGO_DEBUG --app $appName
   heroku config:get DJANGO_ALLOWED_HOSTS --app $appName
   heroku run python manage.py check --deploy --app $appName
   curl.exe -sSI "http://$appHost"
   curl.exe -sS -D - -o NUL "https://$appHost/contact/"
   ```

   The plain-HTTP request should redirect to HTTPS. The HTTPS response should include `Strict-Transport-Security`; the Contact page's CSRF cookie and an authenticated session cookie should include the `Secure` attribute. A `security.W021` deployment-check warning about HSTS preload is expected: preload is intentionally disabled for the Heroku hostname. Check the release output for successful migrations and open the HTTPS site to smoke-test the catalog, registration/login, tracker, community, and contact flows. A deployment is not verified until these checks have been run against the newly released version.

### AI-assisted development reflection

I used the built-in Copilot to support the development of this application, including establishing its structure, refining the user experience, and identifying accessibility improvements informed by WCAG guidance. Copilot also helped me write and run automated tests, investigate bugs, and work through technical issues as I developed and scoped the project.

I encountered several critical errors during development and had to restart the project more than once. Copilot helped me understand and resolve these challenges, and supported me in completing the application on time and to the standard I was aiming for. I reviewed and tested the resulting work as part of the development process.

Because of time constraints and development challenges, I relied heavily on Copilot while building the blog and comments features with Django. Its step-by-step explanations helped me understand the implementation and add these features to the project.

One specific example of this assistance was building browser-test journeys for registration and watchlist updates, community posts and comments, and contact requests. I reviewed the test flows and extended them to check that dismissing a success notification removes it, cancelling a tracker deletion preserves the entry, and confirming the deletion removes it. I also extended the responsive checks across public pages and signed-in tracker/comment pages. The current optional Playwright suite passes all four browser tests, while the separate Django suite verifies model, form, and permission behavior. This testing helped me check Copilot-assisted work against observable results rather than relying on generated code alone.

### Considerations for next updates

- **Improve contact request handling:** Add optional email notifications for staff and an acknowledgement for the sender. Add rate limiting or spam protection before enabling email delivery.
- **Add community moderation tools:** Let staff review or remove inappropriate posts and comments, and give users a way to report content.
- **Expand account support:** Add password-reset and email-verification flows, with clear guidance for users who lose access to their account.
- **Strengthen accessibility verification:** Continue page-by-page keyboard and screen-reader testing, check text and control contrast, and add automated accessibility checks to the development workflow.
- **Expand end-to-end coverage:** Add browser checks for invalid form submissions, logged-out restrictions, and other accessibility interactions as the application evolves.
- **Use durable production media storage:** Store uploaded anime covers in persistent object storage so they remain available across deployments and dyno restarts.
