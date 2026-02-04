# Image Gallery - API/Routes Reference

## Authentication Routes

### Register User
- **URL:** `/register`
- **Methods:** GET, POST
- **Access:** Public
- **Description:** Create new user account
- **Fields:** username, email, password, confirm_password

### Login
- **URL:** `/login`
- **Methods:** GET, POST
- **Access:** Public
- **Description:** Authenticate user
- **Fields:** username, password

### Logout
- **URL:** `/logout`
- **Methods:** GET
- **Access:** Requires Login
- **Description:** Logout current user

---

## Gallery Routes

### View Gallery (Home)
- **URL:** `/` or `/gallery`
- **Methods:** GET
- **Access:** Public (limited to public images), Authenticated (shows all public + own)
- **Pagination:** `?page=1`
- **Description:** Display all public images with pagination

### Upload Image
- **URL:** `/upload`
- **Methods:** GET, POST
- **Access:** Requires Login
- **Description:** Upload new image
- **Fields:** 
  - `file` (required): Image file
  - `title` (required): Image title
  - `description` (optional): Image description
  - `is_public` (optional): Checkbox for visibility
- **Allowed Formats:** JPG, JPEG, PNG, GIF, WebP
- **Max Size:** 16MB

### View Image Details
- **URL:** `/image/<image_id>`
- **Methods:** GET
- **Access:** Public (if public) / Authenticated (if owner or admin)
- **Description:** Display image with details
- **Response:** Image, title, description, uploader info

### Edit Image
- **URL:** `/image/<image_id>/edit`
- **Methods:** GET, POST
- **Access:** Authenticated (owner or admin only)
- **Fields:**
  - `title` (required): New title
  - `description` (optional): New description
  - `is_public` (optional): Visibility toggle

### Delete Image
- **URL:** `/image/<image_id>/delete`
- **Methods:** POST
- **Access:** Authenticated (owner or admin only)
- **Description:** Permanently delete image

### My Images
- **URL:** `/my-gallery`
- **Methods:** GET
- **Access:** Requires Login
- **Pagination:** `?page=1`
- **Description:** View user's uploaded images

---

## Admin Routes

### Admin Dashboard
- **URL:** `/admin/dashboard`
- **Methods:** GET
- **Access:** Admin Only
- **Description:** System overview with statistics
- **Stats Displayed:**
  - Total users
  - Active users
  - Total images
  - Total admins

### Manage Users
- **URL:** `/admin/users`
- **Methods:** GET
- **Access:** Admin Only
- **Pagination:** `?page=1`
- **Description:** List all users with management options

### Toggle User Admin Status
- **URL:** `/admin/user/<user_id>/toggle-admin`
- **Methods:** POST
- **Access:** Admin Only (cannot change own status)
- **Description:** Promote/demote user to/from admin

### Toggle User Active Status
- **URL:** `/admin/user/<user_id>/toggle-active`
- **Methods:** POST
- **Access:** Admin Only (cannot deactivate self)
- **Description:** Activate/deactivate user account

### Delete User
- **URL:** `/admin/user/<user_id>/delete`
- **Methods:** POST
- **Access:** Admin Only (cannot delete self)
- **Description:** Permanently delete user and their images
- **Note:** Cascades deletion of all user's images

### Manage Images
- **URL:** `/admin/images`
- **Methods:** GET
- **Access:** Admin Only
- **Pagination:** `?page=1`
- **Description:** List all images in system

### Delete Image (Admin)
- **URL:** `/admin/image/<image_id>/delete`
- **Methods:** POST
- **Access:** Admin Only
- **Description:** Admin deletion of any image

### Toggle Image Public Status
- **URL:** `/admin/image/<image_id>/toggle-public`
- **Methods:** POST
- **Access:** Admin Only
- **Description:** Make image public or private

---

## Response Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 302 | Redirect (login required, etc.) |
| 404 | Resource not found |
| 405 | Method not allowed |

---

## Authentication Flow

1. **Public User** → Can view only public images
2. **Register** → Create account (user role)
3. **Login** → Start session
4. **Upload** → Add images to gallery
5. **Admin Promotion** → Existing admin promotes user

---

## Permissions Matrix

| Action | Public | User | Admin |
|--------|--------|------|-------|
| View Public Images | ✓ | ✓ | ✓ |
| View Own Private | ✗ | ✓ | ✓ |
| Upload Images | ✗ | ✓ | ✓ |
| Edit Own Images | ✗ | ✓ | ✓ |
| Delete Own Images | ✗ | ✓ | ✓ |
| View All Users | ✗ | ✗ | ✓ |
| Manage Users | ✗ | ✗ | ✓ |
| Manage All Images | ✗ | ✗ | ✓ |
| Access Dashboard | ✗ | ✗ | ✓ |

---

## Error Handling

### Common Error Messages

- **"All fields are required"** - Missing required form field
- **"Passwords do not match"** - Password confirmation mismatch
- **"Password must be at least 6 characters"** - Password too short
- **"Username already exists"** - Chosen username taken
- **"Email already registered"** - Email in use
- **"Invalid username or password"** - Wrong credentials
- **"Your account has been deactivated"** - Account inactive
- **"You do not have permission"** - Access denied
- **"No file selected"** - File upload missing
- **"Invalid file type"** - Unsupported image format
- **"Admin access required"** - Non-admin attempted admin route

---

## Data Validation

### Username
- Required
- Must be unique
- No length restrictions (validated in form)

### Email
- Required
- Must be valid email format
- Must be unique

### Password
- Required
- Minimum 6 characters
- Must match confirmation

### Image Title
- Required
- Max 255 characters

### Image File
- Required for upload
- Allowed: JPG, JPEG, PNG, GIF, WebP
- Max 16MB

---

## Session Management

- **Session Duration:** Browser session (persistent)
- **Remember Me:** Not implemented (can be added)
- **Session Storage:** Server-side (Flask-Login)

---

## Query Parameters

| Route | Param | Type | Default | Example |
|-------|-------|------|---------|---------|
| `/gallery` | page | int | 1 | `?page=2` |
| `/my-gallery` | page | int | 1 | `?page=2` |
| `/admin/users` | page | int | 1 | `?page=1` |
| `/admin/images` | page | int | 1 | `?page=1` |
| `/login` | next | str | / | `?next=/admin/dashboard` |

---

## File Upload Details

### Upload Process
1. Validate file exists
2. Check file extension
3. Validate file size (max 16MB)
4. Generate unique filename (timestamp + original)
5. Open and optimize image (PIL)
6. Resize if exceeds 2000x2000px
7. Save with quality=85
8. Create database record
9. Redirect to gallery

### Filename Format
```
YYYYMMDD_HHMMSS_original-filename.ext
Example: 20260204_143022_sunset.jpg
```

---

## Database Indexes

### Recommended Indexes for Performance
```sql
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_images_user_id ON images(user_id);
CREATE INDEX idx_images_is_public ON images(is_public);
CREATE INDEX idx_images_created_at ON images(created_at);
```

---

## Security Headers (Recommended for Production)

```python
@app.after_request
def set_security_headers(response):
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
```

---

## Rate Limiting (Recommended)

Consider adding for production:
- Login attempts: 5 per 15 minutes
- Upload: 10 images per hour per user
- API calls: 100 per minute

Use Flask-Limiter for implementation.

---

## Future API Endpoints (Not Implemented)

```
- PATCH /image/<id> - Partial update
- DELETE /user/<id> - Direct delete
- POST /comment/<image_id> - Add comment
- GET /user/<username> - User profile
- POST /like/<image_id> - Like image
- GET /search?q=query - Search images
```
