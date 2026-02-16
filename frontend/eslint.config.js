import pluginVue from "eslint-plugin-vue";
import tsParser from "@typescript-eslint/parser";
import tsPlugin from "@typescript-eslint/eslint-plugin";
import vueParser from "vue-eslint-parser";

export default [
  // Vue files
  {
    files: ["src/**/*.vue"],
    languageOptions: {
      parser: vueParser,
      parserOptions: {
        parser: tsParser,
        ecmaVersion: "latest",
        sourceType: "module",
      },
    },
    plugins: {
      vue: pluginVue,
      "@typescript-eslint": tsPlugin,
    },
    rules: {
      // Enable Vue recommended rules
      ...pluginVue.configs["flat/recommended"].rules,
      // Enable TypeScript recommended rules for script blocks
      ...tsPlugin.configs.recommended.rules,
      // Customizations
      "vue/multi-word-component-names": "off", // optional
    },
  },
  // TypeScript/JavaScript files (non-Vue)
  {
    files: ["src/**/*.{js,ts}"],
    languageOptions: {
      parser: tsParser,
      parserOptions: {
        ecmaVersion: "latest",
        sourceType: "module",
      },
    },
    plugins: {
      "@typescript-eslint": tsPlugin,
    },
    rules: {
      ...tsPlugin.configs.recommended.rules,
    },
  },
  // Global ignores (optional)
  {
    ignores: ["node_modules", "dist", "*.config.js"],
  },
];
