import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  value: [],
};

export const accountsSlice = createSlice({
  name: "accounts",
  initialState,
  reducers: {
    setAccounts: (state, action) => {
      state.value = action.payload;
    },
  },
});

export const { setAccounts } = accountsSlice.actions;

export default accountsSlice.reducer;
