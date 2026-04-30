
# 📊 Flask Data Archive Manager

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)
![Seaborn](https://img.shields.io/badge/Seaborn-4E8FB6.svg?style=for-the-badge&logo=Seaborn&logoColor=white)

## 📝 About the Project

This project is a dynamic web application built with **Python** and **Flask** that allows users to manage, input, and export tabular data easily. 

Built with strong **Object-Oriented Programming (OOP)** principles, the application separates the web-routing logic from the data-handling logic. It utilizes **Pandas** to efficiently process batch data submitted via a dynamic HTML form and export it directly to `.csv` files. It also includes visualization capabilities using **Matplotlib** and **Seaborn** to generate insights from the stored data.

### ✨ Key Features
* **Dynamic Frontend:** Users can add multiple rows of data at once using a dynamic JavaScript-powered HTML form.
* **OOP Architecture:** Data manipulation is encapsulated within the `Archive` entity, keeping the Flask routes clean and maintainable.
* **Batch Processing:** Handles multiple data entries simultaneously, converting them into heavily optimized Pandas DataFrames.
* **Data Persistence:** Load existing `.csv` archives or create new ones on the fly.
* **Data Visualization:** Capable of generating graphical representations of the dataset.

---

## ⚙️ How It Works

1. **The Form:** The user navigates to the web interface and fills out product information (Name, Amount, Date, Category). They can click "Adicionar outro item" to generate new input fields dynamically.
2. **The Route:** Upon submission, the Flask route (`app.py`) captures the arrays of data and formats them into a clean Python dictionary of lists.
3. **The Entity:** The route passes this dictionary to the `Archive` class, which uses Pandas to convert the raw dictionary into a DataFrame and concatenates it with any existing data.
4. **The Export:** Finally, the entity saves the updated DataFrame back to a `.csv` file.

---

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

Make sure you have Python installed on your system (Python 3.8+ is recommended).

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/VitorCapeleti/PaymentsManagement.git
cd PaymentsManagement
```

**2. Create a Virtual Environment (Recommended)**
Creating a virtual environment keeps the project's dependencies isolated.
* **Windows:**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
* **macOS/Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

**3. Install Dependencies**
Install the required Python packages using `pip`:
```bash
pip install -r requirements.txt
```

---

## 💻 How to Run the Application

Once your virtual environment is active and dependencies are installed, you can start the Flask server:
```bash
python app.py
```

Alternatively, you can run it using the Flask CLI:
```bash
flask run
```

**Access the App:** Open your web browser and navigate to:
`http://127.0.0.1:5000/`

---

## 📁 Project Structure

* `app.py`: The main entry point containing the Flask routes.
* `entities/archive.py`: Contains the `Archive` class, managing Pandas DataFrame logic and CSV file I/O.
* `operations/graph.py`: Handles data visualization logic.
* `templates/`: Contains the HTML files (e.g., `index.html`).
* `static/`: Contains static assets like CSS stylesheets and JavaScript (if separated).
