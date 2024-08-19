import { createSlice } from "@reduxjs/toolkit";
import { authApi } from "../rtkquery/auth";

const initialState = {
  csrfToken: null,
  wsRefreshToken: null,
};

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    setCsrfToken(state, action) {
      state.csrfToken = action.payload;
    },
    setWsRefreshToken(state, action) {
      state.wsRefreshToken = action.payload;
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
        authApi.endpoints.getWsRefreshToken.matchFulfilled,
        (state, action) => {
          state.wsRefreshToken = action.payload.refreshToken;
        }
      );
  },
});

export const { setCsrfToken, setWsRefreshToken } = authSlice.actions;
export const { reducer: authReducer } = authSlice;
