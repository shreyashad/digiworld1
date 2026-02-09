module.exports = {
  content: [
    "../enrichdigiworld/templates/**/*.html",
    "../home/templates/**/*.html",
    "../search/templates/**/*.html",
    "../whitepapers/templates/**/*.html",
    "./input.css", // optional, ensures Tailwind reads this file too
  ],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {},
  },
  plugins: [],
}
