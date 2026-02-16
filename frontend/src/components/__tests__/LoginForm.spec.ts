import { mount } from "@vue/test-utils";
import { describe, it, expect, vi } from "vitest";
import { createPinia, setActivePinia } from "pinia";
import { useAuthStore } from "@/stores/auth";
import LoginForm from "@/components/auth/LoginForm.vue";

// Mock the store module
vi.mock("@/stores/auth", () => ({
  useAuthStore: vi.fn(),
}));

describe("LoginForm", () => {
  beforeEach(() => {
    // create fresh pinia instance for each test
    setActivePinia(createPinia());
  });

  it("calls store.login with correct credentials", async () => {
    // Create a mock login function
    const mockLogin = vi.fn().mockResolvedValue(undefined);

    // Make useAuthStore return our mock
    vi.mocked(useAuthStore).mockReturnValue({
      login: mockLogin,
    } as ReturnType<typeof useAuthStore>);

    const wrapper = mount(LoginForm);

    await wrapper.find("#username").setValue("testuser");
    await wrapper.find("#password").setValue("secret123");
    await wrapper.find("form").trigger("submit.prevent");

    expect(mockLogin).toHaveBeenCalledWith({
      username: "testuser",
      password: "secret123",
    });
  });
});
