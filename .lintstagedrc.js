module.exports = {
  "aether-forge-app/**/*.{js,jsx,ts,tsx}": [
    "npm run lint:fix --prefix aether-forge-app",
    "npm run format --prefix aether-forge-app"
  ]
};