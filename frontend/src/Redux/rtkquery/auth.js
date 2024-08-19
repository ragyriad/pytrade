import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

const host = window.location.origin;

// Define our single API slice object
export const authApi = createApi({
  reducerPath: "authApi",
  baseQuery: fetchBaseQuery({ baseUrl: host + "/api/wealthsimple" }),
  // The "endpoints" represent operations and requests for this server
  endpoints: (builder) => ({
    getCsrfToken: builder.query({
      query: () => "/auth/csrf",
    }),
    getWsRefreshToken: builder.query({
      query: (args) => {
        return {
          url: "/auth",
          method: "POST",
          headers: {
            "Content-type": "appliation/json",
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
export const { useGetCsrfTokenQuery, useLazyGetWsRefreshTokenQuery } = authApi;
