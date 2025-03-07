import { createSlice } from "@reduxjs/toolkit";
import { authApi } from "../rtkquery/auth";

const initialState = {
  csrfToken: null,
  wealthsimple: null,
};

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    setCsrfToken(state, action) {
      state.csrfToken = action.payload;
    },
    setAuthWealthsimple(state, action) {
      state.wealthsimple = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addMatcher(
        authApi.endpoints.getCsrfToken.matchFulfilled,
        (state, action) => {
          state.csrfToken = action.payload.csrfToken;
        }
      )
      .addMatcher(
        authApi.endpoints.getAuthWealthsimple.matchFulfilled,
        (state, action) => {
          console.log("get WS AUTH Payload");
          console.log(action.payload);
          state.wealthsimple = action.payload;
        }
      );
  },
});

export const { setCsrfToken, setAuthWealthsimple } = authSlice.actions;
export const { reducer: authReducer } = authSlice;
