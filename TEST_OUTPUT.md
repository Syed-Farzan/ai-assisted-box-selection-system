# Test Results

## Command Used

```bash
python manage.py test packaging
```

## Test Output

```text
Found 8 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
........
----------------------------------------------------------------------
Ran 8 tests in 0.005s

OK
Destroying test database for alias 'default'...
```

## Result

All 8 automated tests passed successfully.

The tests covered the following scenarios:

- A product fits normally inside a box.
- A product fits inside a box after rotation.
- A product does not fit dimensionally.
- A box is rejected when the product weight exceeds the box capacity.
- A box is rejected when the total product volume exceeds the box volume.
- When multiple boxes are suitable, the lowest-cost box is selected.
- When suitable boxes have the same cost, the box with the least unused volume is selected.
- When no suitable box exists, the recommendation function returns `None`.

## Overall Status

All implemented recommendation service tests passed successfully with no errors.
