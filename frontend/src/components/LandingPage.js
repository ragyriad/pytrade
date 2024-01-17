import Account from './Account';
import ActivityPage from './ActivityPage';
import OverviewPage from './OverviewPage';
import PropTypes from 'prop-types';
import { setTab } from "../Redux/slices/tabSlice";

import React, { useState } from "react";
import { Provider,useSelector } from 'react-redux';
import { useDispatch } from "react-redux";
import store from '../Redux/store';

import { AppBar, Toolbar, Typography, Tabs, Tab, Box } from '@mui/material';

const LandingPage = () => {
    const dispatch = useDispatch();
    const tab = useSelector((state) => state.tab.value);

    const a11yProps = (index) => {
        return {
          id: `simple-tab-${index}`,
          'aria-controls': `simple-tabpanel-${index}`,
        };
      }
    
      const handleTabChange = (event, tab) => {
        dispatch(setTab(tab))
      };
    
    return (
    <Provider store={store}>
        <React.Fragment>
            <div>

                <AppBar sx={{ bgcolor: "#2E3B55" }} position='sticky'>
                    <Toolbar>
                        <Box sx={{ width: '100%' }}>
                            <Box sx={{  }}> 
                                <Tabs onChange={handleTabChange} value={tab} centered >
                                    <Tab  label="Overview"  {...a11yProps(0)} />
                                    <Tab  label="Activities"  {...a11yProps(1)} />
                                    <Tab  label="Options"  {...a11yProps(2)}/>
                                    <Tab  label="Positions"  {...a11yProps(3)} />
                                </Tabs>
                            </Box>
                        </Box>
                        <Typography variant='h5' component="div">
                            PyTrade
                        </Typography>
                    </Toolbar>
                    
                </AppBar>
                <CustomTabPanel value={tab} index={0}>
                    <OverviewPage />
                </CustomTabPanel>
                <CustomTabPanel value={tab} index={1}>
                    <Account />
                    <ActivityPage />
                </CustomTabPanel>
                <CustomTabPanel value={tab} index={2}>
                    Item Three
                </CustomTabPanel>
                <CustomTabPanel value={tab} index={3}>
                    Positions
                </CustomTabPanel>
            </div>
        </React.Fragment>
    </Provider>
    
    );
}

function CustomTabPanel(props) {
    const { children, value, index, ...other } = props;
  
    return (
      <div
        role="tabpanel"
        hidden={value !== index}
        id={`simple-tabpanel-${index}`}
        aria-labelledby={`simple-tab-${index}`}
        {...other}
      >
        {value === index && (
          <Box sx={{ p: 3 }}>
            <Typography>{children}</Typography>
          </Box>
        )}
      </div>
    );
  }
  
  CustomTabPanel.propTypes = {
    children: PropTypes.node,
    index: PropTypes.number.isRequired,
    value: PropTypes.number.isRequired,
  };

export default LandingPage;


