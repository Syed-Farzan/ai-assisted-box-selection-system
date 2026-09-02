# Box Selection System

A Django-based system that recommends the most suitable shipping box for an ecommerce order based on product dimensions, weight, box capacity, and cost.

## Features

- Manage products, orders, order items, and shipping boxes through Django Admin.
- Validate product and box dimensions and weights.
- Check whether individual products fit inside a box.
- Support product rotation when checking dimensions.
- Check total order weight against box weight capacity.
- Check total order volume against box volume.
- Select the lowest-cost suitable box.
- Use unused volume as a tie-breaker when boxes have the same cost.
- Return the recommended box through a JSON API endpoint.
- Includes automated tests for the recommendation logic and API.

---

# Project Structure

```text
ai-assisted-box-selection-system/
├── box_selection_system/
├── packing/
│   ├── admin.py
│   ├── models.py
│   ├── services.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── requirements.txt
└── README.md
```

---

# Models

## Box

Represents an available shipping box.

Fields:

- Name
- Length
- Width
- Height
- Maximum weight capacity
- Cost

Box dimensions represent the usable internal dimensions.

---

## Product

Represents a product that can be added to an order.

Fields:

- Name
- Length
- Width
- Height
- Weight

---

## Order

Represents a customer order.

An order can contain multiple order items.

---

## OrderItem

Connects an order with a product.

Fields:

- Order
- Product
- Quantity

A product can appear in multiple orders, and an order can contain multiple products.

---

# Assumptions

1. All products and boxes are treated as rectangular cuboids.
2. All dimensions are measured in centimeters.
3. All weights are measured in kilograms.
4. Box dimensions represent usable internal dimensions.
5. Product dimensions, weights, box capacities, and costs must be positive values.
6. Exact fits are considered valid.
7. Products may be rotated in any orientation when checking whether they fit inside a box.
8. Every individual product must fit dimensionally inside the selected box.
9. The total order weight must not exceed the box's maximum weight capacity.
10. For orders containing multiple products, packing feasibility is approximated using total product volume.
11. No additional space is reserved for padding or packing materials.
12. The system recommends one box for the entire order.
13. Full 3D bin-packing and multi-box optimization are outside the scope of this project.
14. Among suitable boxes, the lowest-cost box is selected.
15. If multiple suitable boxes have the same cost, the box with the least unused volume is selected.
16. If there is still a tie, the box with the lowest ID is selected.
17. If no suitable box exists, the system returns no recommendation.

---

# Recommendation Algorithm

The recommendation process works as follows:

1. Receive an order ID.
2. Retrieve the order and its order items.
3. Retrieve the products associated with each order item.
4. Calculate the total order weight.
5. Calculate the total order volume.
6. Retrieve all available boxes.
7. For each box:
   - Check whether every individual product fits inside the box.
   - Product rotation is allowed.
   - Check whether the box can support the total order weight.
   - Check whether the box has sufficient total volume.

8. Add every box that passes all checks to a list of suitable boxes.
9. Sort suitable boxes by:
   - Lowest cost.
   - Least unused volume.
   - Lowest box ID.

10. Return the highest-ranked suitable box.
11. If no suitable box passes all checks, return no suitable box found.

---

# Product Rotation

To support rotation, product and box dimensions are sorted before comparison.

For example:

```text
Product: 30 × 20 × 10
Box:    20 × 30 × 15
```

After sorting:

```text
Product: 10 × 20 × 30
Box:    15 × 20 × 30
```

Each corresponding dimension is compared.

The product fits if all product dimensions are less than or equal to the corresponding box dimensions.

---

# API Endpoint

The system provides an endpoint to get the recommended box for an order.

```text
/orders/<order_id>/recommend-box/
```

## Successful Response

```json
{
  "recommended_box": {
    "id": 1,
    "name": "Medium Box",
    "cost": "50.00"
  }
}
```

## No Suitable Box Response

```json
{
  "message": "No suitable box found"
}
```

---

# Setup Instructions

## 1. Clone the repository

```bash
git clone <repository-url>
cd ai-assisted-box-selection-system
```

## 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment.

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Run migrations

```bash
python manage.py migrate
```

## 5. Create a superuser

```bash
python manage.py createsuperuser
```

## 6. Run the development server

```bash
python manage.py runserver
```

The Django Admin interface will be available at:

```text
/admin/
```

Use the admin interface to create products, boxes, orders, and order items.

---

# Running Tests

Run the automated tests using:

```bash
python manage.py test packing
```

The test suite covers:

- Products fitting normally inside a box.
- Products fitting after rotation.
- Products that do not fit dimensionally.
- Weight capacity rejection.
- Volume rejection.
- Selection of the lowest-cost suitable box.
- Tie-breaking using least unused volume.
- No suitable box scenarios.
- API endpoint responses.

---

# Limitations

This project uses total volume as an approximation for packing multiple products.

Therefore, although every individual product may fit inside a box and the total product volume may be less than the box volume, this does not mathematically guarantee that all products can physically be arranged inside the box.

A production warehouse system could improve this by implementing:

- Full 3D bin-packing.
- Multi-box order splitting.
- Packaging material and padding calculations.
- Product orientation restrictions.
- Fragile item handling.
- Box inventory management.

These features are outside the scope of the current assignment.
