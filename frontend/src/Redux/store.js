import { configureStore, combineReducers } from "@reduxjs/toolkit";
import storage from "redux-persist/lib/storage";
import {
  persistReducer,
  FLUSH,
  REHYDRATE,
  PAUSE,
  PERSIST,
  PURGE,
  REGISTER,
} from "redux-persist";

import setCommissionFilterReducer from "./slices/commissionSlice";
import setAccountFilterReducer from "./slices/accountFilterSlice";
import setActivityTypeFilterReducer from "./slices/activityTypeFilterSlice";
import setAccountsReducer from "./slices/accountsSlice";
import setTabReducer from "./slices/tabSlice";
import { authApi } from "./rtkquery/auth";
import { authReducer } from "./slices/authSlice";
const persistConfig = {
  key: "root",
  storage,
};

const persistedTabReducer = persistReducer(persistConfig, setTabReducer);
const persistedAuthReducer = persistReducer(persistConfig, authReducer);

const combinedReducers = combineReducers({
  tab: persistedTabReducer,
  commissionFilter: setCommissionFilterReducer,
  accountFilter: setAccountFilterReducer,
  activityTypeFilters: setActivityTypeFilterReducer,
  accounts: setAccountsReducer,
  auth: persistedAuthReducer,
  [authApi.reducerPath]: authApi.reducer,
});

const store = configureStore({
  reducer: combinedReducers,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
      },
    }).concat(authApi.middleware),
});

export default store;
