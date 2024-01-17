import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  value: false,
};

export const depositSlice = createSlice({
  name: "deposits",
  initialState,
  reducers: {
    setDepositFilter: (state, action) => {
      state.value = action.payload;
    }
  }
 });

 export const { setDepositFilter} = depositSlice.actions

 export default depositSlice.reducer