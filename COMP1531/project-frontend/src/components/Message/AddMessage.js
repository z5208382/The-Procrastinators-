import axios from 'axios';
import {
  Button,
  TextField,
  InputAdornment,
  IconButton,
  Typography,
} from '@material-ui/core';
import React from 'react';
import SendIcon from '@material-ui/icons/Send';
import TimerIcon from '@material-ui/icons/Timer';
import { makeStyles } from '@material-ui/styles';
import AuthContext from '../../AuthContext';
import {StepContext} from '../Channel/ChannelMessages';
import AddMessageTimerDialog from './AddMessageTimerDialog';
import { useInterval } from '../../utils';
import { useStep } from '../../utils/update';

const useStyles = makeStyles((theme) => ({
  flex: {
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'center',
  },
  input: {
    margin: theme.spacing(1),
    marginRight: 0,
  },
  button: {
    margin: theme.spacing(1),
    marginLeft: 0,
    alignSelf: 'stretch',
  },
  rightIcon: {
    marginLeft: theme.spacing(1),
  },
  standupTimer: {
    margin: theme.spacing(2),
  }
}));

const TIMER_INACTIVE_VALUE = -1;

function AddMessage({ channel_id = '' }) {

  const classes = useStyles();
  const [currentMessage, setCurrentMessage] = React.useState('');
  const [currentTimer, setCurrentTimer] = React.useState(TIMER_INACTIVE_VALUE);
  const [timerDialogOpen, setTimerDialogOpen] = React.useState(false);
  const token = React.useContext(AuthContext);
  let onAdd = React.useContext(StepContext);
  onAdd = onAdd ? onAdd : () => {}; // sanity check

  const isTimerSet = currentTimer !== TIMER_INACTIVE_VALUE;

  const [standupRemaining, setStandupRemaining] = React.useState();
  const [standupEndTime, setStandupEndTime] = React.useState();

  const submitMessage = () => {
    const message = currentMessage.trim();
    if (!message) return;
    setCurrentMessage('');

    /**
     * Sending a message when a standup is active
     * note: probably makes sense that this takes precedence over
     *       starting a standup.
     */
    if (standupRemaining && standupRemaining > 0) {
      axios.post(`/standup/send`, {
        token,
        channel_id: Number.parseInt(channel_id),
        message,
      })
        .then(({ data }) => {
          console.log(data);
          onAdd();
        })
        .catch((err) => {});
      return;
    }

    /**
     * Sending a message when the sendlater timer has been set
     */
    if (isTimerSet) {
      axios.post(`/message/sendlater`, {
        token,
        channel_id: Number.parseInt(channel_id),
        message,
        time_sent: (currentTimer.getTime() / 1000), // ms to s conversion
      })
        .then(({ data }) => {
          console.log(data);
        })
        .catch((err) => {});
      setCurrentTimer(TIMER_INACTIVE_VALUE);
      return;
    }

    /**
     * Starting a standup (any message which starts with /standup)
     */
    if (message.startsWith('/standup')) {
      const re = /\/standup\s+([1-9][0-9]*)/;
      const found = message.match(re);
      if (!found || found.length < 2) {
        alert('Usage: /standup <duration in seconds>');
      } else {
        var length = parseInt(found[1], 10);
        if (isNaN(length) || !Number.isInteger(length)) {
          alert('Usage: /standup <duration in seconds>');
        } else {
          axios.post(`/standup/start`, {
            token,
            channel_id: Number.parseInt(channel_id),
            length,
          })
            .then(({ data }) => {
              const { time_finish } = data;
              setStandupEndTime(time_finish);
              alert(`You've started a standup for ${length} seconds`);
            })
            .catch((err) => {});
        }
      }
      return;
    }

    /**
     * Default message sending behaviour
     */
    axios.post(`/message/send`, {
      token,
      channel_id: Number.parseInt(channel_id),
      message,
    })
      .then(({ data }) => {
        console.log(data);
        onAdd();
      })
      .catch((err) => {});
  };

  useInterval(() => {
    if (standupEndTime > Date.now()/1000) {
      setStandupRemaining(() => Math.round(standupEndTime - Math.round(Date.now()/1000)));
    } else {
      setStandupRemaining()
    }
  }, 1000);

  const checkStandupActive = () => {
    if (standupRemaining > 0) return;
    axios
    .get('/standup/active', { params: { token, channel_id } })
    .then(({ data }) => {
      const { is_active = false, time_finish } = data;
      if (is_active && time_finish) {
        setStandupEndTime(time_finish);
      }
    })
    .catch((err) => {});
  }

  const step = useStep(checkStandupActive, [currentMessage] /* check when user is typing */);

  const keyDown = (e) => {
    if (e.key === 'Enter' && !e.getModifierState('Shift')) {
      e.preventDefault();
      submitMessage();
    }
  };

  return (
    <>
      {standupRemaining > 0 && <Typography variant="caption" className={classes.standupTimer}>
        {`STANDUP ACTIVE: ${standupRemaining} seconds remaining`}
      </Typography>}
      <div className={classes.flex}>
        <TextField
          className={classes.input}
          label="Send a message 💬"
          multiline
          placeholder="..."
          // helperText="Add a new message to this channel!"
          fullWidth
          margin="normal"
          variant="filled"
          onKeyDown={keyDown}
          value={currentMessage}
          onChange={(e) => setCurrentMessage(e.target.value)}
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">
                <IconButton
                  aria-label="toggle visibility"
                  disabled={standupRemaining > 0}
                  onClick={() =>
                    isTimerSet ? setCurrentTimer(-1) : setTimerDialogOpen(true)
                  }
                >
                  <TimerIcon color={isTimerSet ? 'secondary' : undefined} />
                </IconButton>
              </InputAdornment>
            ),
          }}
        />
        <Button
          className={classes.button}
          variant="contained"
          color="primary"
          onClick={submitMessage}
        >
          Send
          <SendIcon className={classes.rightIcon} />
        </Button>
      </div>
      <AddMessageTimerDialog
        open={timerDialogOpen}
        handleClose={() => setTimerDialogOpen(false)}
        onTimerChange={setCurrentTimer}
      />
    </>
  );
}

export default AddMessage;
