import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  value: 0,
};

export const tabSlice = createSlice({
  name: "tab",
  initialState,
  reducers: {
    setTab: (state, action) => {
      state.value = action.payload;
    }
  }
 });

 export const { setTab} = tabSlice.actions

 export default tabSlice.reducer