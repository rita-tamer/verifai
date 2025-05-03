import { useRef, useState, useEffect } from "react";
import { Typography, Box, Button, IconButton, TextField, CircularProgress, Avatar, Grid } from "@mui/material";
import { LinkedIn, GitHub, UploadFile, Send } from "@mui/icons-material";
import './App.scss';
import logo from "./assets/logo.svg";
import cssIcon from "./assets/css.png"
import exifToolIcon from "./assets/exiftool.png"
import flaskIcon from "./assets/flask.png"
import gitIcon from "./assets/github.png"
import htmlIcon from "./assets/html.png"
import jsIcon from "./assets/js.png";
import pythonIcon from "./assets/python.png";
import sightengineIcon from "./assets/sightengine.png";
import sqliteIcon from "./assets/sqlite.png"
import step1Icon from "./assets/step1.png";
import step2Icon from "./assets/step2.png";
import step3Icon from "./assets/step3.png";
import step4Icon from "./assets/step4.png";
import step5Icon from "./assets/step5.png";
import step6Icon from "./assets/step6.png";
import reactIcon from "./assets/react.png";
import verdictIcon from "./assets/verdict.png";
import { Cloud } from "react-icon-cloud";
import ritaImg from "./assets/rita.jpeg";
import InfoIcon from '@mui/icons-material/Info';
import TouchAppIcon from '@mui/icons-material/TouchApp';
import BuildCircleIcon from '@mui/icons-material/BuildCircle';
import MemoryIcon from '@mui/icons-material/Memory';
import ContactMailIcon from '@mui/icons-material/ContactMail';
import { Email } from '@mui/icons-material';


const steps = [
  { id: 1, title: "Upload", description: "", image: step1Icon },
  { id: 2, title: "Analyze", description: "", image: step2Icon},
  { id: 3, title: "Preprocessing", description: "", image: step3Icon},
  { id: 4, title: "Features", description: "", image: step4Icon },
  { id: 5, title: "AI Analysis", description: "", image: step5Icon},
  { id: 6, title: "Results", description: "", image: step6Icon }
];

const handleCopyEmail = () => {
  navigator.clipboard.writeText('ritatamerab@gmail.com')
    .then(() => {
      console.log('Email copied to clipboard');
    })
    .catch(err => {
      console.error('Failed to copy email:', err);
    });
};

console.log("Steps verification:", steps.map(step => ({
  id: step.id,
  title: step.title,
  hasImage: Boolean(step.image),
  imageSrc: step.image
})));
const staticIcons = [cssIcon, exifToolIcon, flaskIcon, gitIcon, htmlIcon, jsIcon, pythonIcon, sightengineIcon, sqliteIcon, reactIcon]
const sectionIcons = {
  about: <InfoIcon />,
  tryIt: <TouchAppIcon />,
  how: <BuildCircleIcon />,
  tech: <MemoryIcon />,
  contact: <ContactMailIcon />
}
const cloudProps = {
  containerProps: {
    style: {
      width: "70%",
    }
  },
  options: {
    clickToFront: 500,
    depth: 1,
    imageScale: 2,
    initial: [0.1, -0.1],
    outlineColour: "#0000",
    reverse: true,
    tooltip: "native",
    tooltipDelay: 0,
    wheelZoom: true
  }
}


export const StaticCloud = () => {
  const cloudIcons = staticIcons.map((icon, index) => (
    <a key={index} href="#" onClick={(e) => e.preventDefault()}>
      <img src={icon} width="42" height="42" alt={`Tech-${index}`} />
    </a>
  ));

  return <Cloud {...cloudProps}>
    {cloudIcons}
  </Cloud>
}
function App() {
  const sections = {
    about: useRef(null),
    tryIt: useRef(null),
    how: useRef(null),
    tech: useRef(null),
    contact: useRef(null),
  };



  const [image, setImage] = useState(null);
  const [verdict, setVerdict] = useState(null);
  const [reason, setReason] = useState("");
  const [analyzing, setAnalyzing] = useState(false);
  const [imageFile, setImageFile] = useState(null);

  const handleScroll = (ref) => {
    ref.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImageFile(file);
      setImage(URL.createObjectURL(file));
    }
  };

  const analyzeImage = async () => {
    if (!imageFile) return;
    setAnalyzing(true);
    const formData = new FormData();
    formData.append("image", imageFile);

    try {
      const response = await fetch("http://localhost:5000/analyze", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      setVerdict(data.result);
      setReason(data.reason);
    } catch (_error) {
      setVerdict("Error");
      setReason("Failed to connect to analysis API.");
    } finally {
      setAnalyzing(false);
    }
  };

  const sectionRefs = Object.values(sections);
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    let accumulatedDelta = 0;
    let lastScrollTime = 0;

    const handleWheel = (e) => {
      const now = Date.now();

      if (now - lastScrollTime > 600) accumulatedDelta = 0;

      accumulatedDelta += e.deltaY;
      lastScrollTime = now;

      const threshold = 300; 

      if (accumulatedDelta > threshold && currentIndex < sectionRefs.length - 1) {
        setCurrentIndex((prev) => {
          const nextIndex = prev + 1;
          sectionRefs[nextIndex].current?.scrollIntoView({ behavior: "smooth" });
          return nextIndex;
        });
        accumulatedDelta = 0;
      } else if (accumulatedDelta < -threshold && currentIndex > 0) {
        setCurrentIndex((prev) => {
          const prevIndex = prev - 1;
          sectionRefs[prevIndex].current?.scrollIntoView({ behavior: "smooth" });
          return prevIndex;
        });
        accumulatedDelta = 0;
      }
    };

    window.addEventListener("wheel", handleWheel, { passive: true });
    return () => window.removeEventListener("wheel", handleWheel);
  }, [currentIndex, sectionRefs]);



  return (
    <Box className="App">
      <Box className="about" ref={sections.about} sx={{ gap: 1 }}>
        <Grid container className="about" sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <img src={logo} alt="LOGO" className="about-img" />
          <Typography variant="h3"sx={{  color: "white",   mt: 1,  mb: 1,   textAlign: "center",   fontWeight: 500,}}>
            Where AI Meets Forensic Verification
          </Typography>
          <Grid item xs={12} md={8} className="text-block" sx={{ padding: 0 }}>
            <Typography   variant="h6"   sx={{    width: "100%",    textAlign: "center",    fontSize: "1.5rem",    lineHeight: 1.4  }}>
              Keeping up with the current technological advancements in the field of generative AI, VerifAI aims to achieve a more robust verification schema for images that have been generated, altered, or tampered with using AI models.
            </Typography>
          </Grid>
        </Grid>
      </Box>

      <Box className="try" ref={sections.tryIt}>
        <Grid container className="try">
          <Grid item xs={12} md={6} className="upload-box">
            {!image && <><label htmlFor="upload-input">
              <Box className="drop-box">
                <UploadFile fontSize="large" />
                <Typography >Click to upload!</Typography>
              </Box>
            </label>
              <input id="upload-input" type="file" accept="image/*" onChange={handleImageUpload} hidden /></>}
            {image && <img src={image} alt="preview" className="preview" />}
            {image && <Button variant="cont</Grid>ained" onClick={() => setImage(null)}>Remove</Button>}
          </Grid>
          <Grid item xs={12} md={6} className="verdict-box" sx={{ gap: 2 }}>
            {!image ? (
              <Typography sx={{ width: "100%", textAlign: "center", fontSize: "1.5rem", lineHeight: 1.4 }}>
                Upload a picture to try it out!
              </Typography>
            ) : (
              <Box sx={{ 
                display: 'flex', 
                flexDirection: 'column', 
                alignItems: 'center',
                gap: 2,
                width: '100%',
                maxWidth: '600px',
                margin: '0 auto'
              }}>
                <Button 
                  variant="contained" 
                  disabled={analyzing} 
                  onClick={analyzeImage}
                  sx={{ 
                    width: 'fit-content',
                    minWidth: '120px'
                  }}
                >
                  {analyzing ? <CircularProgress size={24} /> : "Analyze"}
                </Button>
                
                {verdict && (
                  <Box sx={{ 
                    display: 'flex', 
                    flexDirection: 'column', 
                    alignItems: 'center',
                    gap: 1,
                    width: '100%',
                    padding: '1rem',
                    backgroundColor: 'rgba(255, 255, 255, 0.05)',
                    borderRadius: '8px'
                  }}>
                    <Box sx={{ 
                      display: 'flex', 
                      alignItems: 'center',
                      gap: 2,
                      marginBottom: 1
                    }}>
                      <img 
                        src={verdictIcon} 
                        alt="Verdict Icon" 
                        style={{ 
                          height: '50px',
                          objectFit: 'contain'
                        }} 
                      />
                      <Typography variant="h6" sx={{ color: 'white' }}>
                        Verdict: {verdict}
                      </Typography>
                    </Box>
                    <Typography sx={{ 
                      color: 'white',
                      textAlign: 'center',
                      fontSize: '1.1rem'
                    }}>
                      Reason: {reason}
                    </Typography>
                  </Box>
                )}
              </Box>
            )}
          </Grid>
        </Grid>
      </Box>
      
      <Box className="how" ref={sections.how}>
        <Box sx={{ width: '100%',overflowX: "auto", '&::-webkit-scrollbar': { height: '8px' },'&::-webkit-scrollbar-track': { background: '#f1f1f1' },'&::-webkit-scrollbar-thumb': { background: '#888' },'&::-webkit-scrollbar-thumb:hover': { background: '#555' } }} >
        <Grid 
          container 
          className="how" 
          sx={{ 
            flexWrap: "nowrap",
            minWidth: "max-content",
            padding: "2rem",
            gap: 2,
            justifyContent: "flex-start"
          }}
        >
          {steps.map((step) => (
            <Grid item key={step.id} sx={{   width: "250px",  flexShrink: 0,  padding: "1rem",  display: "flex",  flexDirection: "column",  alignItems: "center"}}>
              <img src={step.image} alt={`Step ${step.id}`}style={{   width: "100%",  height: "400px",  objectFit: "contain",  marginBottom: "1rem"}}  />
            </Grid>
          ))}
        </Grid>
      </Box>
      </Box>
    
      <Box className="tech" ref={sections.tech}>
        <Grid container className="tech">
          <Grid item xs={12} md={6}><Typography variant="h4">Technologies Used</Typography></Grid>
          <div
            className="vertical-line"
            style={{
              borderLeft: "2px solid #fff",
              height: "400px",
              left: "50%",
              top: 0,
              transform: "translateX(-50%)",
            }}
          />
          <Grid item xs={6} md={3} className="tech-cloud">
            <StaticCloud />
          </Grid>
        </Grid>
      </Box>

      <Box className="contact" ref={sections.contact}>
        <Grid container className="contact">
          <Grid item xs={12} md={6} sx={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: "1rem",
            padding: "2rem",
            }}>
            <Typography variant="h4">Contact Me</Typography>
            <Avatar
              src={ritaImg}
              alt="Rita T. Ayoub"
              sx={{ width: "150px", height: "150px", marginBottom: "1rem" }}
            />
            <Typography variant="h4" sx={{fontWeight: "bold"}}>Rita T. Ayoub</Typography>
            <div
              style={{
                display: "flex",
                gap: "1.5rem",
                marginTop: "1rem",
              }}
            >
              <IconButton href="https://linkedin.com/in/rita-ayoub" target="_blank" sx={{ fontSize: "2rem" }}><LinkedIn fontSize="inherit" /></IconButton>
              <IconButton href="https://github.com/rita-tamer/verifai" target="_blank" sx={{ fontSize: "2rem" }}><GitHub fontSize="inherit" /></IconButton>
              <IconButton onClick={handleCopyEmail} sx={{ fontSize: "2rem" }}   title="Click to copy Rita's email address!"> <Email fontSize="inherit" /></IconButton>
            </div>
          </Grid>
          
        </Grid>
      </Box>

      <nav>
        {Object.entries(sections).map(([key, ref]) => (
          <IconButton key={key} onClick={() => handleScroll(ref)} sx={{ fontSize: "2rem" }}>
            <Avatar sx={{ width: "50px", height: "50px", backgroundColor: "rgba(0, 0, 0, 0)" }}>
              {sectionIcons[key]}
            </Avatar>
          </IconButton>
        ))}
      </nav>
    </Box>
  );
}

export default App;
