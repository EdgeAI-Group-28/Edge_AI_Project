import React from 'react';
import { Box, Container, Typography, Grid, Card, CardContent, Table, TableHead, TableRow, TableCell, TableBody } from '@mui/material';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css'; 

const bottleData = [
  { time: '10:00 AM', count: 120, lowLiquid: 2 },
  { time: '11:00 AM', count: 135, lowLiquid: 3 },
  { time: '12:00 PM', count: 150, lowLiquid: 1 },
];

const motorTemp = 65; 

function App() {
  return (
    <Box sx={{ width: '100vw', height: '100vh', backgroundColor: 'black', overflow: 'auto', color: 'white' }}>
      <Container maxWidth={false} disableGutters sx={{ padding: 2 }}>
        <Typography variant="h3" align="center" gutterBottom>
          Bottle Conveyor Dashboard
        </Typography>

        {/* Summary cards */}
        <Grid container spacing={2} justifyContent="center" sx={{ marginBottom: 4 }}>
          {/* Summary Cards */}
          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ minWidth: 200 }}>
              <CardContent>
                <Typography variant="h6">Total Bottles Today</Typography>
                <Typography variant="h4">405</Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ minWidth: 200 }}>
              <CardContent>
                <Typography variant="h6">Low Liquid Bottles</Typography>
                <Typography variant="h4">6</Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ minWidth: 200 }}>
              <CardContent>
                <Typography variant="h6">System Status</Typography>
                <Typography variant="h4" color="green">Online</Typography>
              </CardContent>
            </Card>
          </Grid>

          {/* Motor Temp Gauge */}
          <Grid item xs={12} sm={6} md={3} sx={{ marginBottom: 4 }} >
            <Card sx={{ minWidth: 200, height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: 2 }}>
              <Typography variant="h6" gutterBottom>Motor Temperature</Typography>
              <div style={{ width: 100, height: 100 }}>
                <CircularProgressbar
                  value={motorTemp}
                  maxValue={100}
                  text={`${motorTemp}°C`}
                  styles={buildStyles({
                    pathColor: motorTemp > 80 ? 'red' : motorTemp > 60 ? 'orange' : 'green',
                    textColor: '#000',
                    trailColor: '#d6d6d6',
                  })}
                />
              </div>
            </Card>
          </Grid>
        </Grid>

        {/* Table */}
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>Bottle Counts Per Hour</Typography>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Time</TableCell>
                  <TableCell>Number of Bottles</TableCell>
                  <TableCell>Low Liquid Detected</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {bottleData.map((row, index) => (
                  <TableRow key={index}>
                    <TableCell>{row.time}</TableCell>
                    <TableCell>{row.count}</TableCell>
                    <TableCell>{row.lowLiquid}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </Container>
    </Box>
  );
}

export default App;
