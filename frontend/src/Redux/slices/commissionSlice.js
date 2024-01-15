import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  value: false,
};

export const commissionSlice = createSlice({
  name: "commissionFilter",
  initialState,
  reducers: {
    setCommissionFilter: (state, action) => {
      state.value = action.payload;
    }
  }
 });

 export const { setCommissionFilter } = commissionSlice.actions

 export default commissionSlice.reducer