import { configureStore, combineReducers } from "@reduxjs/toolkit";
import setTabReducer from "./slices/tabSlice";
import storage from "redux-persist/lib/storage";
import {
  persistStore,
  persistReducer,
  FLUSH,
  REHYDRATE,
  PAUSE,
  PERSIST,
  PURGE,
  REGISTER,
} from "redux-persist";
import thunk from "redux-thunk";

import setCommissionFilterReducer from "./slices/commissionSlice";
import setAccountFilterReducer from "./slices/accountFilterSlice";
import setTradesFilterReducer from "./slices/commissionSlice";
import setDepositsFilterReducer from "./slices/accountFilterSlice";
import setActivityTypeFilterReducer from "./slices/activityTypeFilterSlice";
import setAccountsReducer from "./slices/accountsSlice";

const persistConfig = {
  key: "root",
  storage,
};

const persistedReducer = persistReducer(persistConfig, setTabReducer);

const combinedReducers = combineReducers({
  tab: persistedReducer,
  commissionFilter: setCommissionFilterReducer,
  accountFilter: setAccountFilterReducer,
  activityTypeFilters: setActivityTypeFilterReducer,
  accounts: setAccountsReducer,
});

const store = configureStore({
  reducer: combinedReducers,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
      },
    }),
});

export default store;
