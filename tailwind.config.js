/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html", // Pour tous les templates Django
    "./*/templates/**/*.html", // Pour les templates dans les apps Django
    "./static/src/**/*.js",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

