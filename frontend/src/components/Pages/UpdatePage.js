// import React, { useState } from "react";
// import { useSelector } from "react-redux";
// import axios from "axios";

// import { Grid, Button, Paper, Snackbar } from "@mui/material";

// const fetchData = async (refreshToken, csrfToken, account_id = null) => {
//   try {
//     let syncActivitiesUrl = new URL(
//       "http://localhost:8000/api/wealthsimple/activity"
//     );
//     const data = {
//       refreshToken: refreshToken,
//       account_id: account_id,
//     };
//     const response = await axios({
//       method: "POST",
//       url: syncActivitiesUrl,
//       headers: {
//         "X-CSRFToken": csrfToken,
//       },
//       data,
//     });
//     return response.data;
//   } catch (error) {
//     console.error("Error fetching data:", error);
//     return null;
//   }
// };

// const UpdatePage = () => {
//   const [data, setData] = useState(null);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState(null);

//   let refreshToken = useSelector((state) => state.auth.wsRefreshToken);
//   let csrfToken = useSelector((state) => state.auth.csrfToken);

//   const updateBroker = async (Broker) => {
//     if (Broker === "Wealthsimple") {
//       const fetchDataAsync = async () => {
//         const result = await fetchData(refreshToken, csrfToken, null);
//         if (result) {
//           setData(result);
//         } else {
//           setError("Error loading data");
//         }
//         setLoading(false);
//       };

//       fetchDataAsync();
//     }
//   };

//   return (
//     <Grid>
//       <Paper sx={{ p: 2 }}>
//         <Grid container spacing={2} justifyContent={"center"}>
//           <Grid item>
//             <Button
//               variant="contained"
//               size="medium"
//               onClick={() => updateBroker("Questrade")}
//             >
//               Questrade
//             </Button>
//           </Grid>
//           <Grid item>
//             <Button
//               variant="contained"
//               size="medium"
//               onClick={() => updateBroker("Wealthsimple")}
//             >
//               Wealthsimple
//             </Button>
//           </Grid>
//         </Grid>
//       </Paper>
//     </Grid>
//   );
// };

// export default UpdatePage;
import React, { useState } from "react";
import { useSelector } from "react-redux";
import axios from "axios";
import { Grid, Button, Paper, Snackbar } from "@mui/material";
import WealthsimpleAuthModal from "../Modals/WealthsimpleAuthModal";

const fetchData = async (refreshToken, csrfToken, account_id = null) => {
  try {
    let syncActivitiesUrl = new URL(
      "http://localhost:8000/api/wealthsimple/activity"
    );
    const data = {
      refreshToken: refreshToken,
      account_id: account_id,
    };
    const response = await axios({
      method: "POST",
      url: syncActivitiesUrl,
      headers: {
        "X-CSRFToken": csrfToken,
      },
      data,
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error; // Throw the error to be caught in updateBroker
  }
};

const UpdatePage = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [snackbarOpen, setSnackbarOpen] = useState(false);

  let refreshToken = useSelector((state) => state.auth.wsRefreshToken);
  let csrfToken = useSelector((state) => state.auth.csrfToken);

  const handleModalClose = () => {
    setModalOpen(false);
  };

  const handleSnackbarClose = () => {
    setSnackbarOpen(false);
  };

  const handleMfaSubmit = async (mfaCode) => {
    try {
      setLoading(true);
      const result = await fetchData(refreshToken, csrfToken, null, mfaCode);
      setData(result);
      setError(null);
    } catch (error) {
      console.error(error);
      if (error.status == 401) {
        setError("MFA Code is incorrect, please try again.");
        setModalOpen(true);
      }
    } finally {
      setLoading(false);
    }
  };

  const updateBroker = async (Broker) => {
    if (Broker === "Wealthsimple") {
      setLoading(true);
      try {
        await fetchData(refreshToken, csrfToken, null);
        setSnackbarOpen(true); // Show snackbar after request is sent
      } catch (error) {
        setError("An error occurred. Please enter your MFA code.");
        setModalOpen(true);
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <Grid>
      <WealthsimpleAuthModal
        open={modalOpen}
        handleClose={handleModalClose}
        handleSubmit={handleMfaSubmit}
        errorMessage={error}
      />
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={3000}
        onClose={handleSnackbarClose}
        message="Request sent"
      />
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
