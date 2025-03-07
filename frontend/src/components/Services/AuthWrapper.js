import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import {
  useGetCsrfTokenQuery,
  useGetAuthWealthsimpleMutation,
} from "../../Redux/rtkquery/auth";
import {
  setCsrfToken,
  setAuthWealthsimple,
} from "../../Redux/slices/authSlice";
import WealthsimpleAuthModal from "../Modals/WealthsimpleAuthModal";
import LandingPage from "../Pages/LandingPage";

const AuthWrapper = () => {
  const dispatch = useDispatch();
  const csrfToken = useSelector((state) => state.auth.csrfToken);
  const wsRefreshToken = useSelector((state) => state.auth.wsRefreshToken);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [twoFaError, setTwoFaError] = useState(null);

  const {
    data: csrfTokenData,
    isLoading: isCsrfLoading,
    error: csrfError,
  } = useGetCsrfTokenQuery();

  const [authWealthsimple, { isLoading: isAuthLoading, error: refreshError }] =
    useGetAuthWealthsimpleMutation();

  useEffect(() => {
    const fetchTokens = async () => {
      if (authWealthsimple) {
        console.log(authWealthsimple);
      }
      if (csrfTokenData && !csrfToken) {
        const csrfToken = csrfTokenData.csrf_token;
        dispatch(setCsrfToken(csrfToken));
        if (!wsRefreshToken) setIsModalOpen(true);
      }
    };

    if (csrfTokenData && !csrfToken) {
      fetchTokens();
    }
  }, [csrfTokenData, csrfToken, wsRefreshToken, authWealthsimple, dispatch]);

  const handleModalClose = () => {
    setIsModalOpen(false);
    setTwoFaError(null); // Reset the error state when the modal closes
  };

  const handleAuthSubmit = async (twoFaCode) => {
    if (csrfToken) {
      try {
        const result = await authWealthsimple({
          csrfToken,
          twoFaCode,
        }).unwrap();
        const wsAuth = result;
        console.log("WS AUTH");
        console.log(wsAuth);
        dispatch(setAuthWealthsimple(wsAuth));
        setIsModalOpen(false);
        setTwoFaError(null); // Reset any previous errors
      } catch (error) {
        console.log(error);
        // Check if the error is a 401 or 400 and open the modal if it is
        if (error?.status === 401 || error?.status === 400) {
          console.log(
            "Failed to Fetch Refresh Token with status:",
            error.status
          );
          setTwoFaError(`${error.data.error_message}! Please try again.`);
          setIsModalOpen(true); // Open the modal for user to enter MFA code again
        } else {
          console.log("Unexpected error:", error);
          setTwoFaError(
            "An unexpected error occurred. Please try again later."
          );
        }
      }
    }
  };

  if (csrfError || refreshError) {
    console.error("Error fetching tokens:", csrfError || refreshError);
  }

  return (
    <>
      <WealthsimpleAuthModal
        open={isModalOpen}
        handleClose={handleModalClose}
        handleAuthSubmit={handleAuthSubmit}
        errorMessage={twoFaError} // Pass the error message to the modal
      />
      {console.log(
        `crsf => ${csrfToken} \n wsRefreshToken => ${wsRefreshToken}`
      )}
      {csrfToken && wsRefreshToken ? (
        <LandingPage handleAuthSubmit={handleAuthSubmit} />
      ) : (
        <div />
      )}
    </>
  );
};

export default AuthWrapper;
