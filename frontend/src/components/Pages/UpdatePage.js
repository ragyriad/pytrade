import React, { useState } from "react";
import { useSelector } from "react-redux";
import axios from "axios";
import { Grid, Button, Paper } from "@mui/material";
import { API_URLS } from "../../config";

const UpdatePage = ({ handleAuthSubmit }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  let refreshToken = useSelector((state) => state.auth.wsRefreshToken);
  let csrfToken = useSelector((state) => state.auth.csrfToken);

  const fetchData = async (accessToken, csrfToken, account_id = null) => {
    try {
      const data = {
        refreshToken: accessToken,
        account_id: account_id,
      };
      const response = await axios({
        method: "POST",
        url: `${API_URLS.PROD_BASE + API_URLS.WS + API_URLS.ACTIVITY}`,
        headers: {
          "X-CSRFToken": csrfToken,
        },
        data,
      });
      return response.data;
    } catch (error) {
      if (error.response) {
        const status = error.response.status;
        const message =
          error.response.data.error_message || "An error occurred";
        throw { status, message }; // Throw an object with status and message
      } else {
        // Handle errors where error.response does not exist
        throw { status: 500, message: "Network Error" }; // Generic error message
      }
    }
  };

  const updateBroker = async (Broker) => {
    if (Broker === "Wealthsimple") {
      setLoading(true);
      try {
        await fetchData(refreshToken, csrfToken, null);
      } catch (error) {
        console.log("Update Page Error");
        console.log(error);
        setError(error.message);
        if (error.status === 401) {
          setModalOpen(true);
        } else if (error.status === 400) {
          setError("MFA Code is incorrect, please try again.");
          setModalOpen(true);
        } else {
          console.log("Handle Error");
          console.log(error.message);
        }
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <Grid>
      <Paper sx={{ p: 2 }}>
        <Grid container spacing={2} justifyContent={"center"}>
          <Grid item>
            <Button
              variant="contained"
              size="medium"
              onClick={() => updateBroker("Questrade")}
            >
              Questrade
            </Button>
          </Grid>
          <Grid item>
            <Button
              variant="contained"
              size="medium"
              onClick={() => updateBroker("Wealthsimple")}
            >
              Wealthsimple
            </Button>
          </Grid>
        </Grid>
      </Paper>
    </Grid>
  );
};

export default UpdatePage;
