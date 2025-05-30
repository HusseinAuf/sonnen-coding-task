# 🔋 sonnenBatterie Energy Algorithm Tests

This test suite verifies the **energy management algorithm** of the `sonnenBatterie` system using `pytest`.

---

## ✅ What It Tests

The energy algorithm decides how power flows between:

- **Photovoltaics (PV)**
- **Battery Storage**
- **House**
- **Grid**

It follows these rules:

1. **When PV > House Consumption**

   - Charge the battery (if not full)
   - Export extra power to the grid (if battery is full)

2. **When House Consumption > PV**
   - Discharge battery (if not empty)
   - Import from grid (if battery is empty)

---

## 🧪 Test Scenarios

- `test_pv_exceeds_house_consumption_and_storage_not_full`
- `test_pv_exceeds_house_consumption_and_storage_full`
- `test_house_consumption_exceeds_pv_and_storage_not_empty`
- `test_house_consumption_exceeds_pv_and_storage_empty`
