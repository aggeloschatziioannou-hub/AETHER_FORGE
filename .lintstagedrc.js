module.exports = {
  "aether-forge-app/src/**/*.{js,jsx,ts,tsx}": [
    "npm run lint --prefix aether-forge-app",
    "npm run format:fix --prefix aether-forge-app"
  ]
};