import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  value: [],
};

export const activityTypeFilterSlice = createSlice({
  name: "activityTypeFilter",
  initialState,
  reducers: {
    setActivityTypeFilter: (state, action) => {
      state.value = action.payload;
    },
  },
});

export const { setActivityTypeFilter } = activityTypeFilterSlice.actions;

export default activityTypeFilterSlice.reducer;
