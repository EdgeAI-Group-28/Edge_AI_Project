import React, { useEffect, useState } from 'react';
import {Box,Container,Typography,Grid,Card,CardContent,Table,TableHead,TableRow,TableCell,TableBody} from '@mui/material';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';



function App() {

    
const [motorTemp, setMotorTemp] = useState(0);


const [bottleSize, setBottleSize] = useState([]);
const [fillingLevel, setFillingLevel] = useState([]);
const [temperatureData, setTemperatureData] = useState([]);

  useEffect(() => {
    const getLatestData = async () => {
      const url = `https://6v9iws76pe.execute-api.ap-south-1.amazonaws.com/Production`;

      try {
        const response = await fetch(url);
        const data = await response.json();
        const parsedBody = JSON.parse(data.body);

        // No filtering, just store all entries
        setBottleSize(parsedBody.result.Bottle_Size || []);
        setFillingLevel(parsedBody.result.Filling_Level || []);
        setTemperatureData(parsedBody.result.temperature_data || []);

        console.log("Bottle Sizes:", parsedBody.result.Bottle_Size);
        console.log("Filling Levels:", parsedBody.result.Filling_Level);
        console.log("Temperature Data:", parsedBody.result.temperature_data);

      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    const intervalId = setInterval(() => {
      getLatestData();
    }, 1);

    return () => clearInterval(intervalId);
  }, []);




  const [command, setCommand] = useState("");
  const [result, setResult] = useState(null);  

  const handleExecute = async () => {
  if (!command.trim()) return alert("Please enter a command");

  try {
    const response = await fetch("https://668d-175-157-38-252.ngrok-free.app/execute", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ command }),
    });

    const data = await response.json();
    console.log("API Response:", data);
    setResult(data);  // Save the result to display below

  } catch (error) {
    console.error("Error executing command:", error);
    setResult({ error: "Failed to execute command" });
  }
};

const [predictions, setPredictions] = useState([]);

  useEffect(() => {
  // Generate dummy prediction data for next 5 days
  const generatePredictions = () => {
    const today = new Date();
    const newPredictions = [];

    for (let i = 0; i < 5; i++) {
      const date = new Date(today);
      date.setDate(today.getDate() + i);

      const formattedDate = date.toISOString().split('T')[0]; // YYYY-MM-DD
      const randomValue = Math.floor(Math.random() * 200) + 200; // Random temp 200–400

      newPredictions.push({
        date: formattedDate,
        value: randomValue
      });
    }

    setPredictions(newPredictions);
  };

  generatePredictions();
}, []);



  
const PredictionsTable = () => {
  // Generate dates from today up to 5 days
  const generateDateRange = () => {
    const dates = [];
    const today = new Date();
    for (let i = 0; i < 5; i++) {
      const date = new Date(today);
      date.setDate(today.getDate() + i);
      dates.push(date.toISOString().split('T')[0]); // Format as YYYY-MM-DD
    }
    return dates;
  };

  // Create dummy prediction data
  const predictionData = generateDateRange().map(date => ({
    date,
    predicted_bottle_count: Math.floor(Math.random() * 100) + 50 // random number between 50-150
  }));

}


























  return (

   <>


    <Box sx={{ width: '100vw', height: '100%', backgroundColor: 'black', color: 'white', pb: 4 }}>
      <Container maxWidth={false} disableGutters sx={{ padding: 2 }}>
        <Typography variant="h3" align="center" gutterBottom>
          Bottle Conveyor Dashboard
        </Typography>

        {/* Summary cards */}
        <Grid container spacing={2} justifyContent="center" sx={{ marginBottom: 4 }}>
          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ minWidth: 200 }}>
              <CardContent>
                <Typography variant="h6">Total Bottles Today</Typography>
                <Typography variant="h4"></Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ minWidth: 200 }}>
              <CardContent>
                <Typography variant="h6">Low Liquid Bottles</Typography>
                <Typography variant="h4"></Typography>
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

          <Grid item xs={12} sm={6} md={3}>
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



      <Box sx={{ marginBottom: 4, marginLeft: 2, marginRight: 2 }}>
        <Card sx={{ width: '100%' }}>
          <CardContent>
            <Typography variant="h6" gutterBottom><b>Bottle Sizes</b></Typography>
            <Table sx={{ minWidth: 650 }}>
              <TableHead>
                <TableRow>
                  <TableCell>Device ID</TableCell>
                  <TableCell>Size</TableCell>
                  <TableCell>Timestamp</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {bottleSize.length === 0 ? (
                  <TableRow><TableCell colSpan={3}><i>Not available data yet</i></TableCell></TableRow>
                ) : (
                  bottleSize.map((item, index) => (
                    <TableRow key={index}>
                      <TableCell>{item.device_id ?? "null"}</TableCell>
                      <TableCell>{item.size ?? "null"}</TableCell>
                      <TableCell>{item.timestamp ?? "null"}</TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </Box>







       <Box sx={{ marginBottom: 4, marginLeft: 2, marginRight: 2 }}>
        <Card sx={{ width: '100%' }}>
          <CardContent>
            <Typography variant="h6" gutterBottom><b>Filling Levels</b></Typography>
            <Table sx={{ minWidth: 650 }}>
              <TableHead>
                <TableRow>
                  <TableCell>Device ID</TableCell>
                  <TableCell>Level</TableCell>
                  <TableCell>Timestamp</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {fillingLevel.length === 0 ? (
                  <TableRow><TableCell colSpan={3}>Not available data</TableCell></TableRow>
                ) : (
                  fillingLevel.map((item, index) => (
                    <TableRow key={index}>
                      <TableCell>{item.device_id ?? "null"}</TableCell>
                      <TableCell>{item.level ?? "null"}</TableCell> 
                      <TableCell>{item.timestamp ?? "null"}</TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </Box>
     

    
{/* Motor Temperature Table */}
<Box sx={{ marginBottom: 4, marginLeft: 2, marginRight: 2 , color: "black"}}>
  <Card sx={{ width: '100%' ,  backgroundColor: 'white' }}>
    <CardContent>
      <Typography variant="h6" gutterBottom><b>Motor Temperature</b></Typography>
      <Table sx={{ minWidth: 650 }}>
        <TableHead>
          <TableRow>
            <TableCell>Time</TableCell>
            <TableCell>Motor Temperature (°C)</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {temperatureData.length === 0 ? (
            <TableRow><TableCell colSpan={2}><i>Not available data yet</i></TableCell></TableRow>
          ) : (
            temperatureData.map((item, index) => (
              <TableRow key={index}>
                <TableCell>{item.time ?? "null"}</TableCell>
                <TableCell>{item.motor_temp ?? item.celsius ?? "null"}</TableCell>
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
    </CardContent>
  </Card>
</Box>



          
    
<Box sx={{ marginBottom: 4, marginLeft: 2, marginRight: 2 , color: "black"}}>
  <Card sx={{ width: '100%' ,  backgroundColor: 'white' }}>
    <CardContent>
      <Typography variant="h6" gutterBottom><b>Count Predictions</b></Typography>
      <Table sx={{ minWidth: 650 }}>
        <TableHead>
          <TableRow>
            <TableCell>DateTime</TableCell>
            <TableCell>Predicted Count</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
       
              <TableRow >
                <TableCell>2025-05-25 06:00:00</TableCell>
                <TableCell>11</TableCell>
              </TableRow>

              <TableRow >
                <TableCell>2025-05-25 07:00:00</TableCell>
                <TableCell>14</TableCell>
              </TableRow>

              <TableRow >
                <TableCell>2025-05-25 08:00:00</TableCell>
                <TableCell>20</TableCell>
              </TableRow>
           
        </TableBody>
      </Table>
    </CardContent>
  </Card>
</Box>





















  <div className="d-flex justify-content-center" style={{ background: "black", padding: "1rem 0" }}>
    <div className="input-group" style={{ marginLeft: -2, marginRight: -2, width: "90%" }}>
      <input type="text" className="form-control" placeholder="$> Enter the command to execute" value={command} onChange={(e) => setCommand(e.target.value)} />
      <button className="btn btn-secondary" type="button" style={{ width: "160px", textAlign: "center" }} onClick={handleExecute}><b>Execute</b></button>
    </div>
  </div>


  {result && (
  <div style={{ marginTop: "1rem", color: "white" }}>
    <h5>Output:</h5>
    <pre style={{ backgroundColor: "#333", padding: "1rem", borderRadius: "5px" }}>
      {result.output || "No output"}
    </pre>

    {result.error && (
      <>
        <h5>Error:</h5>
        <pre style={{ backgroundColor: "#3a0000", padding: "1rem", borderRadius: "5px", color: "#ff9999" }}>
          {result.error}
        </pre>
      </>
    )}
  </div>
)}





 </Container>
  </Box>





    </>
  );
}

export default App;
