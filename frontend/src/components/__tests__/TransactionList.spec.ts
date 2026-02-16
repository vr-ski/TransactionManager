import { mount } from "@vue/test-utils";
import { describe, it, expect } from "vitest";
import TransactionList from "@/components/transactions/TransactionList.vue";

describe("TransactionList", () => {
  const mockTransactions = [
    {
      transaction_id: 1,
      contractor_from: "Alice",
      contractor_to: "Bob",
      amount: 100.5,
      transaction_type: "Card Payment",
      status: {
        status_id: 1,
        code: "completed",
        display_name: "Completed",
        color: "green",
      },
      created_at: "2026-02-15T10:00:00Z",
    },
    {
      transaction_id: 2,
      contractor_from: "Bob",
      contractor_to: "Charlie",
      amount: 75.25,
      transaction_type: "Transfer",
      status: {
        status_id: 2,
        code: "pending",
        display_name: "Pending",
        color: "yellow",
      },
      created_at: "2026-02-14T09:30:00Z",
    },
  ];

  it("renders all transactions", () => {
    const wrapper = mount(TransactionList, {
      props: {
        transactions: mockTransactions,
        selectedId: null,
      },
    });

    const items = wrapper.findAll(".transaction-item");
    expect(items).toHaveLength(2);

    expect(items[0].text()).toContain("Alice → Bob");
    expect(items[0].text()).toContain("100.5");
    expect(items[0].text()).toContain("Completed");
  });

  it("emits select event when clicked", async () => {
    const wrapper = mount(TransactionList, {
      props: {
        transactions: mockTransactions,
        selectedId: null,
      },
    });

    await wrapper.find(".transaction-item").trigger("click");
    expect(wrapper.emitted("select")).toBeTruthy();
    expect(wrapper.emitted("select")[0][0]).toBe(1); // first transaction id
  });

  it("highlights selected transaction", () => {
    const wrapper = mount(TransactionList, {
      props: {
        transactions: mockTransactions,
        selectedId: 2,
      },
    });

    const items = wrapper.findAll(".transaction-item");
    expect(items[1].classes()).toContain("selected");
  });
});
