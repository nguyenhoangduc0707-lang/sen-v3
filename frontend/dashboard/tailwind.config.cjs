/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        glass: "rgba(255,255,255,0.12)",
        "glass-border": "rgba(255,255,255,0.18)"
      },
      backdropBlur: {
        xs: "4px",
        sm: "8px",
        md: "12px"
      },
      borderRadius: {
        xl: "1rem"
      },
      boxShadow: {
        glass: "0 4px 30px rgba(0,0,0,0.1)"
      },
      transitionProperty: {
        bg: "background-color, border-color, color, fill, stroke, opacity, box-shadow, transform"
      }
    }
  },
  plugins: []
};
