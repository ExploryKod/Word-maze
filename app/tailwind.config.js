const path = require("path");

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    path.join(__dirname, "templates/**/*.html"),
    path.join(__dirname, "static/**/*.js"),
    path.join(__dirname, "node_modules/flowbite/**/*.js"),
  ],
  theme: {
    extend: {},
  },
  plugins: [require("flowbite/plugin")],
};
