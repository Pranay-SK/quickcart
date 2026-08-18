# QuickCart - Quick-Commerce Grocery Delivery Platform

A feature-rich Django-based quick-commerce marketplace platform specializing in grocery delivery. QuickCart connects customers with nearby shops to deliver fresh groceries in minutes. The platform supports multi-shop management, location-based ordering, and secure payment processing.

## Key Features

### 🛒 For Customers
- **User Registration & Email Verification**: Sign up with email verification link activation
- **Location-Based Shop Discovery**: Automatic geolocation to find nearest shops with distance calculation
- **Product Browsing**: Browse grocery items by category across multiple shops
- **Smart Cart Management**: Add/remove items with real-time cart updates
- **Order Placement**: Place orders with location-based fastest delivery from nearest shop
- **Payment Integration**: Secure Razorpay payment gateway integration with order review option
- **Delivery Information Management**: Edit delivery address at final checkout stage
- **Password Reset**: Secure password reset via email verification link
- **Customer Dashboard**: View total orders, logged-in status, recent order history
- **My Orders**: View all orders with invoice download via detail button, order tracking
- **Profile Settings**: Upload/update profile picture, cover photo, personal information (name, phone, address)
- **Google Maps Integration**: Automatic address geocoding (country, state, city, postal code, latitude, longitude)
- **Quick Logout**: One-click logout functionality

### 🏪 For Shop Owners
- **Shop Registration & Verification**: Submit shop details including license for admin verification
- **Admin Approval Process**: Email notifications for shop approval/rejection with activation link
- **Shop Dashboard**: Overview of total orders, revenue, and monthly statistics
- **Shop Management**: Update shop profile, cover image, license, address with Google Maps integration
- **Inventory Management**: Add/remove products by category with availability status
- **Operating Hours**: Set weekly operating hours, close days, and holiday closures
- **Order Management**: View and manage all customer orders in real-time
- **Revenue Tracking**: Monitor total revenue and monthly revenue analytics
- **Shop Status Badge**: Display open/closed status on marketplace
- **Quick Logout**: One-click logout functionality

### 🔧 General Features
- **Multi-Role Support**: Automatic role detection (Customer, Shop Owner, Admin)
- **Top Navigation Bar**: Cart icon, Marketplace icon, My Account/Logout
- **Responsive Design**: Mobile-friendly interface for all devices
- **Tax Calculation**: Automatic CGST and SGST calculation on orders
- **Order Tracking**: Real-time order status and delivery updates
- **Admin Panel**: Complete Django admin interface for system management

## Project Structure

```
quickcart/
├── accounts/         # User authentication and profile management
├── customers/        # Customer data and management
├── items/            # Product listings and categories
├── marketplace/      # Marketplace views and functionality
├── orders/           # Order processing and management
├── shop/             # Seller shop management
├── quickcart/        # Project settings and configuration
├── media/            # User-uploaded files (images, etc.)
├── static/           # Static assets (CSS, JS, images)
├── templates/        # HTML templates
├── env/              # Python virtual environment
├── db.postgresql     # postgresql database
└── manage.py         # Django management script
```

## Requirements

- Python 3.8+
- Django 3.0+
- PostgreSQL (or SQLite for development)
- GDAL 3.12.2 (for geographic features)
- Pillow 12.3.0 (for image processing)
- Razorpay 2.0.1 (for payment processing)

### Project Dependencies

```
asgiref==3.11.1
certifi==2026.7.22
charset-normalizer==3.5.0
Django==6.0.6
GDAL==3.12.2
idna==3.18
pillow==12.3.0
psycopg2==2.9.12
python-decouple==3.8
razorpay==2.0.1
requests==2.34.2
simplejson==4.1.1
sqlparse==0.5.5
tzdata==2026.2
urllib3==2.7.0
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git (for version control)
- PostgreSQL (optional, for production)

### 1. Clone or Download the Repository
```bash
cd quickcart
```

### 2. Create Virtual Environment (if not already created)
```bash
python -m venv env
```

### 3. Activate Virtual Environment
- **Windows (PowerShell)**:
  ```powershell
  .\env\Scripts\Activate.ps1
  ```
- **Windows (Command Prompt)**:
  ```cmd
  env\Scripts\activate.bat
  ```
- **Linux/macOS**:
  ```bash
  source env/bin/activate
  ```

### 4. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Create a `.env` file in the project root directory:
```
DEBUG=True
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_secret
```

### 6. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```
Follow the prompts to set up your admin username, email, and password.

### 8. Collect Static Files (for production)
```bash
python manage.py collectstatic --noinput
```

### 9. Run Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## User Workflows

### 👥 Customer Workflow

1. **Registration**
   - Navigate to login/register page
   - Enter first name, last name, email, username, and password
   - Verification email sent to registered email
   - Click activation link in email to verify account
   - Log in with credentials

2. **Browsing & Shopping**
   - Homepage displays featured products and "Fresh Groceries, Delivered In Minutes" banner
   - Use search bar with product name and location filters
   - Browse products by category
   - View shops sorted by distance (nearest shop on top)
   - Live location capture shows distance to each shop

3. **Cart Management**
   - Add products from selected shops to cart
   - View cart with item details, quantity, and pricing
   - See real-time tax calculations (CGST, SGST)
   - Modify quantities or remove items

4. **Checkout & Payment**
   - Proceed to checkout from cart
   - Review/edit billing address using Google Maps geocoding:
     - First Name, Last Name
     - Phone Number, Email
     - Street Address
     - Country, State, City, Postal Code
     - Latitude, Longitude (auto-filled)
   - Select payment method (Razorpay)
   - Complete payment
   - Option to edit delivery information at final stage

5. **Order Management**
   - View order confirmation and details
   - Access order invoice
   - Track delivery status in real-time
   - View order history in "My Orders" section

6. **Account Management**
   - **Dashboard**: View total orders count, logged-in email, recent order history
   - **My Orders**: Table with Order ID, Name, Total, Status, Date, and Action buttons
   - **Profile Settings**: 
     - Upload/update profile picture
     - Upload/update cover photo
     - Edit personal information (first name, last name, phone)
     - Manage delivery address with Google Maps integration
   - **Password Management**: Reset password via email verification link
   - **Logout**: Quick logout option

### 🏪 Shop Owner Workflow

1. **Shop Registration**
   - Click "REGISTER SHOP" button on website
   - Enter personal details (first name, last name)
   - Enter shop details:
     - Shop name
     - Shop license
     - Email
     - Username
     - Password
   - Submit for verification

2. **Admin Verification**
   - Admin reviews submitted shop details
   - Verification email sent to shop owner:
     - **If Approved**: Activation link to activate shop
     - **If Rejected**: Rejection notice with feedback

3. **Shop Dashboard**
   - **Dashboard Overview**:
     - Total Orders count
     - Total Revenue
     - This Month Revenue
     - Recent Orders (last 5 orders with details)
   - **My Shop**: Update shop profile, cover image, license, and address
   - **Add Items**: 
     - Add products by category
     - Set product availability status
     - Upload product images
     - Set pricing
   - **Opening Hours**: 
     - Set weekly operating hours
     - Define open/close times for each day
     - Set closed days or holidays
     - Status displayed on marketplace
   - **Orders**: 
     - View all customer orders
     - Track order status
     - Manage order fulfillment
   - **Shop Status Badge**: 
     - Display "OPEN" or "CLOSED" on marketplace
     - Auto-updated based on opening hours
   - **Logout**: Quick logout option

## Access Control

The application automatically detects user roles and displays appropriate dashboards:
- **Customers**: Customer dashboard with orders and profile
- **Shop Owners**: Shop dashboard with inventory and revenue
- **Admins**: Full Django admin panel with system management



## Application URLs & Routes

### Public Routes
- `/` - Home page with product listings
- `/accounts/login/` - Customer login
- `/accounts/register/` - Customer registration
- `/accounts/register-shop/` - Shop owner registration
- `/accounts/password-reset/` - Password reset page

### Customer Routes
- `/accounts/custdashboard/` - Customer dashboard
- `/customers/` - Customer information
- `/items/` - Product catalog
- `/marketplace/` - Marketplace view (all shops)
- `/orders/` - Orders management
- `/cart/` - Shopping cart

### Shop Owner Routes
- `/accounts/shopperdashboard/` - Shop owner dashboard
- `/shop/` - Shop management

### Admin Routes
- `/admin/` - Django admin panel
- `/admin/accounts/` - User management
- `/admin/shop/` - Shop management
- `/admin/items/` - Product management
- `/admin/orders/` - Order management
- `/admin/marketplace/` - Tax management

## Testing

### Running Tests

Run the complete test suite:
```bash
python manage.py test
```

Run tests for specific apps:
```bash
# Test accounts app
python manage.py test accounts

# Test orders app
python manage.py test orders

# Test shop app
python manage.py test shop

# Test with verbose output
python manage.py test --verbosity=2

# Run specific test module
python manage.py test accounts.tests.TestUserRegistration

# Run tests and create coverage report
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Test Organization
- `accounts/tests.py` - User authentication and profile tests
- `orders/tests.py` - Order management and payment tests
- `shop/tests.py` - Shop management tests
- `items/tests.py` - Product catalog tests
- `marketplace/tests.py` - Marketplace functionality tests

## Technologies & Dependencies

### Core Framework
- **Django 6.0.6** - Web framework
- **Python 3.8+** - Programming language
- **PostgreSQL/SQLite** - Database

### Payment Processing
- **Razorpay 2.0.1** - Payment gateway integration

### Geospatial Features
- **GDAL 3.12.2** - Geographic data abstraction library
- **Google Maps API** - Geocoding and location services

### Image Processing
- **Pillow 12.3.0** - Image library for product images and user avatars

### Database & ORM
- **psycopg2 2.9.12** - PostgreSQL adapter
- **SQLAlchemy** - ORM support
- **sqlparse 0.5.5** - SQL parsing

### HTTP & Utilities
- **requests 2.34.2** - HTTP library
- **urllib3 2.7.0** - HTTP client
- **simplejson 4.1.1** - JSON encoder/decoder

### Security & Environment
- **python-decouple 3.8** - Environment variable management
- **certifi 2026.7.22** - SSL certificate verification
- **charset-normalizer 3.5.0** - Character encoding

### Server & Deployment
- **asgiref 3.11.1** - ASGI utilities
- **tzdata 2026.2** - Timezone database

## Development

### Project Architecture

**Django Apps:**
- **accounts**: User authentication, registration, profiles, password reset
- **customers**: Customer data and management
- **shop**: Shop owner dashboard and management
- **items**: Product catalog, categories, inventory
- **marketplace**: Marketplace functionality, shop listings, location-based search
- **orders**: Order processing, payment integration, tracking
- **quickcart**: Project settings, middleware, URL routing

### Adding New Features

1. **Create a new Django app**:
   ```bash
   python manage.py startapp myapp
   ```

2. **Define models** in `myapp/models.py`:
   ```python
   from django.db import models
   
   class MyModel(models.Model):
       name = models.CharField(max_length=100)
       created_at = models.DateTimeField(auto_now_add=True)
   ```

3. **Create views** in `myapp/views.py`:
   ```python
   from django.shortcuts import render
   
   def my_view(request):
       return render(request, 'myapp/template.html')
   ```

4. **Configure URLs** in `myapp/urls.py`:
   ```python
   from django.urls import path
   from . import views
   
   urlpatterns = [
       path('', views.my_view, name='my_view'),
   ]
   ```

5. **Register the app** in `quickcart/settings.py`:
   ```python
   INSTALLED_APPS = [
       # ... existing apps
       'myapp',
   ]
   ```

6. **Create and apply migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

### Database Migrations

```bash
# Create migration files for model changes
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# Show migration status
python manage.py showmigrations

# Rollback migrations
python manage.py migrate app_name 0001

# Create empty migration
python manage.py makemigrations --empty app_name --name migration_name
```

### Common Development Commands

```bash
# Create superuser for admin access
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Run with different port
python manage.py runserver 8080

# Run shell for interactive queries
python manage.py shell

# Clear cache
python manage.py clear_cache

# Collect static files
python manage.py collectstatic

# Check deployment configuration
python manage.py check --deploy
```

## Static Files & Media Management

### Static Files

Static files include CSS, JavaScript, fonts, and images used across the site.

```bash
# Collect all static files for production
python manage.py collectstatic

# Clear existing static files before collecting
python manage.py collectstatic --clear --noinput

# Collect without user confirmation
python manage.py collectstatic --noinput
```

**Static File Structure:**
```
static/
├── css/              # Stylesheets (Bootstrap, custom CSS)
├── js/               # JavaScript files
├── images/           # Icons and graphics
├── fonts/            # Custom fonts
├── extra-images/     # Additional image assets
└── logo/             # Logo variations
```

**In Development:**
- Django serves static files automatically when `DEBUG=True`
- Static files are served from `quickcart/static/`

**In Production:**
- Configure web server (Nginx/Apache) to serve static files
- Use CDN for better performance
- Update `STATIC_ROOT` in settings.py

### Media Files

User-uploaded content including product images, shop logos, and profile pictures.

**Media Directory Structure:**
```
media/
├── productimages/    # Product photos
├── users/
│   ├── profile_pictures/     # User profile avatars
│   └── cover_photos/         # User cover images
└── Shops/
    └── licenses/     # Shop license documents
```

**Permissions & Storage:**
- Images are validated for security
- Maximum file size limits enforced
- Automatic image optimization for web
- In production, consider using AWS S3 or Cloud Storage

**Accessing Media Files:**
- User profile: `/media/users/profile_pictures/{username}.jpg`
- Cover photo: `/media/users/cover_photos/{username}.jpg`
- Product image: `/media/productimages/{product_id}.jpg`
- Shop license: `/media/Shops/licenses/{shop_id}.pdf`

## Database

### Development
The project uses SQLite (`db.sqlite3`) by default for development, making it easy to set up and test locally.

### Production
For production environments, configure PostgreSQL:

1. Install PostgreSQL
2. Create a database:
   ```bash
   psql -U postgres
   CREATE DATABASE quickcart_db;
   CREATE USER quickcart_user WITH PASSWORD 'your_password';
   ALTER ROLE quickcart_user SET client_encoding TO 'utf8';
   ALTER ROLE quickcart_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE quickcart_user SET default_transaction_deferrable TO on;
   GRANT ALL PRIVILEGES ON DATABASE quickcart_db TO quickcart_user;
   \q
   ```

3. Update `.env`:
   ```
   DATABASE_URL=postgresql://quickcart_user:your_password@localhost:5432/quickcart_db
   ```

4. Install PostgreSQL adapter:
   ```bash
   pip install psycopg2-binary
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

## Database Models

- **User**: Django built-in User model extended with profiles
- **UserProfile**: Customer profile with location, preferences
- **Shop**: Shop information, license, address
- **Category**: Product categories
- **Product**: Items with pricing, shop association, images
- **Cart**: Shopping cart management
- **Order**: Order tracking and management
- **OrderedProduct**: Individual items in orders
- **Payment**: Payment records with Razorpay integration
- **Tax**: CGST and SGST configuration

## Environment Variables

Create a `.env` file in the project root with the following configuration:

```env
# Django Configuration
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
ENVIRONMENT=development

# Database Configuration
DATABASE_URL=sqlite:///db.sqlite3
# For PostgreSQL: DATABASE_URL=postgresql://user:password@localhost:5432/quickcart_db

# Razorpay Payment Gateway
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret

# Email Configuration (optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

# Google Maps API (for geocoding)
GOOGLE_MAPS_API_KEY=your_google_maps_api_key

# AWS S3 (optional, for media storage in production)
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
```

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -m "Add your feature"`
3. Push to branch: `git push origin feature/your-feature`
4. Submit a pull request

## Troubleshooting

### Database Issues

**Error: Table already exists**
```bash
python manage.py migrate --fake-initial
```

**Clear all data and start fresh**
```bash
python manage.py flush --no-input
python manage.py migrate
python manage.py createsuperuser
```

**Database locked**
```bash
# Remove SQLite database and recreate
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

**PostgreSQL connection issues**
```bash
# Check PostgreSQL is running
# Verify DATABASE_URL in .env
# Test connection: psql -U user -h localhost -d database_name
```

### Missing Dependencies

**Import errors**
```bash
# Reinstall all requirements
pip install --upgrade pip
pip install -r requirements.txt

# Check installed packages
pip list

# Show dependency tree
pip install pipdeptree
pipdeptree
```

**GDAL installation issues** (for geographic features)
```bash
# Windows: Download from https://trac.osgeo.org/gdal/wiki/DownloadingGdalBinaries
# Ubuntu/Debian:
sudo apt-get install gdal-bin libgdal-dev

# macOS:
brew install gdal
```

### Static Files Issues

**Static files not loading**
```bash
# Clear and recollect static files
python manage.py collectstatic --clear --noinput

# Rebuild static files cache
python manage.py collectstatic --no-input

# Check static files configuration in settings.py
# Ensure STATIC_URL and STATIC_ROOT are configured
```

**CSS/JS files 404 errors**
```bash
# Verify STATIC_URL setting (usually '/static/')
# Check static files exist in static/ directory
# Ensure web server is configured to serve from STATIC_ROOT
```

### Media Upload Issues

**Permission denied when uploading media**
```bash
# Check media directory permissions
chmod -R 755 media/

# Verify MEDIA_URL and MEDIA_ROOT in settings.py
```

**Image upload failures**
```bash
# Check Pillow installation
pip install --upgrade Pillow

# Verify image format compatibility
# Ensure file size is within limits (settings.py)
```

### Authentication & Login Issues

**User cannot login**
```bash
# Check user account exists
python manage.py shell
from django.contrib.auth.models import User
User.objects.all()

# Reset password
python manage.py changepassword username

# Check user is_active status
user = User.objects.get(username='username')
print(user.is_active)
user.is_active = True
user.save()
```

**Email verification not working**
```bash
# Check email backend in settings.py
# Test email sending:
python manage.py shell
from django.core.mail import send_mail
send_mail('Test', 'Message', 'from@example.com', ['to@example.com'])
```

**Session/Cache issues**
```bash
# Clear all sessions
python manage.py clearsessions

# Clear cache
python manage.py clear_cache
```

### Payment Integration Issues

**Razorpay API errors**
```bash
# Verify RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET in .env
# Check Razorpay account is in Live mode (not Test mode)
# Verify API keys are correct
# Check network connectivity
```

**Payment webhook failures**
```bash
# Test webhook in Razorpay dashboard
# Verify webhook URL is publicly accessible
# Check server logs for webhook delivery
```

### Location/Maps Issues

**Google Maps not loading**
```bash
# Verify GOOGLE_MAPS_API_KEY in .env
# Check API key has required permissions (Maps, Geocoding)
# Verify API key restrictions allow your domain
# Check browser console for errors
```

**Geocoding API errors**
```bash
# Ensure Google Maps Geocoding API is enabled
# Check API quota hasn't been exceeded
# Verify address format before sending to API
```

### Performance Issues

**Slow page loads**
```bash
# Run Django Debug Toolbar to identify bottlenecks
pip install django-debug-toolbar

# Check database queries with:
python manage.py shell
from django.db import connection
from django.test.utils import CaptureQueriesContext
with CaptureQueriesContext(connection) as context:
    # Your code here
    pass
print(f"Queries: {len(context)}")

# Enable caching in settings.py
# Use pagination for large datasets
```

**High memory usage**
```bash
# Profile memory with:
pip install memory-profiler
python -m memory_profiler manage.py runserver
```

### Help & Support

1. **Check Django logs**:
   ```bash
   # Enable logging in settings.py
   # Check logs/ directory
   ```

2. **Use Django shell for debugging**:
   ```bash
   python manage.py shell
   from path.to.model import YourModel
   obj = YourModel.objects.first()
   print(obj)
   ```

3. **Enable DEBUG mode for detailed error messages** (development only):
   ```
   DEBUG=True  # in .env
   ```

4. **Check error logs**:
   ```bash
   # Django development server console
   # Application logs in logs/ directory
   # System event logs
   ```

## Contributing

We welcome contributions to QuickCart! Here's how to contribute:

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/quickcart.git
   cd quickcart
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow Django best practices
   - Write clean, documented code
   - Add tests for new features
   - Update README if needed

4. **Test your changes**
   ```bash
   python manage.py test
   python manage.py check --deploy
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add descriptive commit message"
   ```

6. **Push to your branch**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Submit a Pull Request**
   - Provide clear description of changes
   - Link any related issues
   - Ensure tests pass

## Code Style Guidelines

- Follow PEP 8 Python style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused
- Use type hints where applicable

```python
def get_user_orders(user_id: int) -> list:
    """
    Retrieve all orders for a specific user.
    
    Args:
        user_id: The ID of the user
        
    Returns:
        List of Order objects
    """
    from orders.models import Order
    return Order.objects.filter(user_id=user_id).order_by('-created_at')
```

## Security & Best Practices

- Never commit sensitive data (.env files, secrets)
- Always validate user input
- Use Django's built-in security features
- Keep dependencies updated
- Run security checks: `python manage.py check --deploy`
- Use HTTPS in production
- Implement proper authentication and authorization

## License

This project is provided as-is for educational and commercial use. 

**© 2026 QuickCart. All rights reserved.**
**Developed by: Pranay Khairnar**

For commercial licensing inquiries, please contact: khairarpranay@gmail.com

## Support & Contact

### Getting Help

1. **Documentation**: Check this README first
2. **Issues**: Search existing GitHub issues
3. **Discussions**: Join our community discussions
4. **Stack Overflow**: Tag questions with `django` and `quickcart`

### Contact Information

- **Developer**: Pranay Khairnar


### Reporting Issues

Found a bug? Please create an issue with:
- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, Django version)
- Screenshots if applicable

### Feature Requests

Have a great idea? Submit a feature request with:
- Detailed description
- Use cases
- Proposed implementation (if possible)
- Related issues or discussions

## Deployment

### Deploy to Production

#### Using Gunicorn & Nginx

1. **Install Gunicorn**
   ```bash
   pip install gunicorn
   ```

2. **Create Gunicorn service file** (`/etc/systemd/system/gunicorn_quickcart.service`)
   ```ini
   [Unit]
   Description=Gunicorn service for QuickCart
   After=network.target

   [Service]
   Type=notify
   User=www-data
   Group=www-data
   WorkingDirectory=/path/to/quickcart
   EnvironmentFile=/path/to/.env
   ExecStart=/path/to/env/bin/gunicorn --workers 3 --bind unix:/path/to/gunicorn.sock quickcart.wsgi:application

   [Install]
   WantedBy=multi-user.target
   ```

3. **Configure Nginx** (`/etc/nginx/sites-available/quickcart`)
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;

       location / {
           proxy_pass http://unix:/path/to/gunicorn.sock;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       location /static/ {
           alias /path/to/quickcart/static/;
       }

       location /media/ {
           alias /path/to/quickcart/media/;
       }
   }
   ```

4. **Enable SSL with Let's Encrypt**
   ```bash
   sudo apt-get install certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com
   ```


