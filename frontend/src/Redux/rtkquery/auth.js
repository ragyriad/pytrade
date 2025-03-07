import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { API_URLS } from "../../config.js";

// Define our single API slice object
export const authApi = createApi({
  reducerPath: "authApi",
  baseQuery: fetchBaseQuery({
    baseUrl: API_URLS.PROD_BASE,
  }),
  // The "endpoints" represent operations and requests for this server
  endpoints: (builder) => ({
    getCsrfToken: builder.query({
      query: () => API_URLS.CSRF,
    }),
    getAuthWealthsimple: builder.mutation({
      query: (args) => {
        return {
          url: API_URLS.WS + API_URLS.AUTH,
          method: "POST",
          headers: {
            "Content-type": "application/json",
            "X-CSRFToken": args.csrfToken,
            mode: "same-origin",
          },
          body: args.twoFaCode,
        };
      },
    }),
  }),
});

// Export the auto-generated hook for the `getPosts` query endpoint
export const { useGetCsrfTokenQuery, useGetAuthWealthsimpleMutation } = authApi;
