import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  value: false,
};

export const tradeSlice = createSlice({
  name: "trade",
  initialState,
  reducers: {
    setTradeFilter: (state, action) => {
      state.value = action.payload;
    }
  }
 });

 export const { setTradeFilter} = tradeSlice.actions

 export default tradeSlice.reducer