You are tasked with refactoring an existing POS (Point of Sale) web interface built with Flask + Jinja into a reusable component-based UI system using **Neumorphism design principles (soft, accessible variant)**.

Your goal is to create reusable UI components and integrate them into the existing checkout page without breaking functionality.

---

# 🔧 TECH STACK REQUIREMENTS

* Backend: Flask (unchanged)
* Template engine: Jinja2
* Frontend:

  * Tailwind CSS (REQUIRED)
  * Vanilla JavaScript (minimal)
* No heavy frameworks (React/Vue not allowed)

---

# 🎯 DESIGN GOAL

Implement **soft neumorphism (not full)** with:

* subtle dual shadows (light + dark)
* good contrast for readability
* maintain usability for POS (fast interaction, clear visibility)

---

# 🎨 DESIGN TOKENS (DEFINE FIRST)

Create a global design system using CSS variables or Tailwind config:

Colors:

* Background: #2b2f3a
* Light shadow: #373b49
* Dark shadow: #1f222b
* Primary accent: #ff6ec7
* Text: #e4e6eb

Shadows:

* Raised:
  6px 6px 12px dark,
  -6px -6px 12px light

* Inset:
  inset 6px 6px 12px dark,
  inset -6px -6px 12px light

Border radius:

* Card: 20px
* Button: 12px–50% (circle for icon buttons)
* Input: 12px

---

# 🧩 COMPONENTS TO BUILD

## 1. 🧱 Card Component

Reusable container for sections like:

* "Pilih Produk"
* "Pembayaran"
* "Ringkasan"

Requirements:

* soft raised neumorphism
* padding: 16–24px
* rounded-xl (20px)
* optional header slot

Variants:

* default
* hover (slightly stronger shadow)

---

## 2. 🔘 Button Component

Variants:

* primary (accent color)
* neutral (default neumorphism)
* icon button (for + / -)

States:

* default → raised
* hover → slightly brighter
* active → inset (pressed effect)

Behavior:

* must support:

  * text buttons
  * icon-only buttons
  * disabled state

---

## 3. ⌨️ Input Component

Use for:

* quantity input
* payment input

Style:

* inset neumorphism
* no harsh borders
* focus state:

  * slight glow or accent outline

Support:

* type="text"
* type="number"

---

## 4. 🔘 Radio / Select Component (IMPORTANT)

For:

* product selection
* "eceran / lusinan"

Requirements:

* custom styled (not default browser UI)
* outer: neumorphism
* inner: accent when selected

---

# 🧱 FILE STRUCTURE

Organize components:

/templates/components/
card.html
button.html
input.html
radio.html

/static/css/
neumorphism.css

/static/js/
ui.js

---

# 🔁 JINJA COMPONENT USAGE

Each component must be reusable using Jinja include/macros.

Example:

```jinja
{% include "components/button.html" with context %}
```

OR use macros:

```jinja
{% from "components/button.html" import button %}
{{ button("Tambah", variant="primary") }}
```

---

# 🔄 INTEGRATION INTO EXISTING POS UI

Refactor the current checkout page:

## Replace:

* Product container → Card component
* Qty buttons (+ / -) → Icon Button component
* Qty input → Input component
* Dropdown (Tipe Jual) → Styled select/radio component

---

# ⚠️ UX CONSTRAINTS (VERY IMPORTANT)

* Do NOT reduce readability
* Do NOT remove contrast from text
* Keep table layout clear (do NOT neumorph everything)
* Only apply neumorphism to:

  * cards
  * buttons
  * inputs

---

# ⚡ INTERACTION REQUIREMENTS

* Button click must feel “pressable” (inset effect)
* Quantity update must still work (JS preserved)
* No lag or heavy animations

---

# 🧪 TESTING CHECKLIST

* Buttons visually press when clicked
* Inputs are readable and usable
* Works on dark background
* No layout breaking in existing POS page

---

# 🚀 OPTIONAL ENHANCEMENTS

* Add hover animation (shadow shift)
* Add focus ring (accessible)
* Add dark/light toggle (if time permits)

---

# 📦 OUTPUT EXPECTATION

* Clean reusable components
* Minimal duplication
* Easy to extend
* Fully integrated into checkout page

---
