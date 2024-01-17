import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  value: [],
};

export const accountFilterSlice = createSlice({
  name: "accountFilter",
  initialState,
  reducers: {
    setAccountFilter: (state, action) => {
      state.value = action.payload;
    }
  }
 });

 export const { setAccountFilter } = accountFilterSlice.actions

 export default accountFilterSlice.reducer