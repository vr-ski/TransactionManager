declare module "*.vue" {
  import type { DefineComponent } from "vue";
  // Using DefineComponent with generic arguments that avoid any and {}
  const component: DefineComponent<object, object, unknown>;
  export default component;
}
