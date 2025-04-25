
# 🐾 Pet Friend

**Pet Friend** is a Django-based web application designed to offer an all-in-one solution for pet owners. Whether you're looking to book grooming services, purchase pet supplies, or manage your pet’s profile, Pet Friend is your go-to digital companion.

## 🚀 Features

- 🛍️ **Product Store** – Browse and buy pet food, toys, and more.
- 🧼 **Service Booking** – Book grooming, vet visits, and other pet care services.
- 🔒 **User Authentication** – Sign up/login with secure sessions.
- 📋 **Pet Profile Management** – Add, edit, and view your pet’s details.
- 🛒 **Cart System** – Add/remove both products and services to your cart.
- 💳 **Razorpay Integration** – Smooth and secure payment gateway.
- 📅 **Time Slot Booking System** – Prevents double-booking of services.
- 📈 **Admin Dashboard** – Fully integrated with Django Admin for backend control.

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **Backend**: Python 3, Django Framework
- **Database**: MySQL
- **Payment Gateway**: Razorpay (Test Mode)
- **Version Control**: Git & GitHub

## 🧑‍💻 Setup Instructions

1. **Clone the Repository**  
```bash
git clone https://github.com/your-username/pet-friend.git
cd pet-friend
```

2. **Create & Activate Virtual Environment**  
```bash
python3 -m venv env
source env/bin/activate
```

3. **Install Requirements**  
```bash
pip install -r requirements.txt
```

4. **Configure MySQL Database**  
- Create a MySQL database named `petfriend`
- Update your `settings.py` with your DB credentials

5. **Run Migrations & Start Server**  
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## 📸 Screenshots

> Add screenshots here from your `/screenshots` folder  
> `![Home Page](screenshots/home.png)`

## 📌 Upcoming Features

- Email notifications for bookings
- User reviews and ratings
- Order tracking for products
- Admin analytics dashboard

## 🙋‍♂️ Developer

**Harshil Chauhan**  
📧 harshilworks082@gmail.com  
📱 +91 6354731425  
🎓 BCA – Chimanbhai Institute of Computer Applications, Gujarat University

## 🤝 Contributions

PRs are welcome! Just fork, code, and create a pull request. Let's make pet care smarter together. 💡

## 📄 License

This project is licensed under the MIT License.

---

> *"Because pets aren't just animals — they're family."*
