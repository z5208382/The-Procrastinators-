import React from 'react';
import axios from 'axios';

import { List, ListSubheader, Button, ListItem } from '@material-ui/core';
import { useStep } from '../../utils/update';
import Message from '../Message';
import AuthContext from '../../AuthContext';
import AddMessage from '../Message/AddMessage';
import { PAGINATION_SIZE, SLICE_SIZE } from '../../utils/constants';


export const StepContext = React.createContext();
export const StepProvider = StepContext.Provider;
export const StepConsumer = StepContext.Consumer;

function ChannelMessages({ channel_id = '' }) {

  const [messages, setMessages] = React.useState([]);
  const [pagination, setPagination] = React.useState({
    "channelId": channel_id,
    "isPaginating": false,
    "currentStart": 0,
    "currentEnd": 0,
    "sliceStart": 0,
  })
  const token = React.useContext(AuthContext);

  const fetchChannelMessages = () => {
    const p = pagination.channelId === channel_id
        ? pagination
        : {
          "channelId": channel_id,
          "isPaginating": false,
          "currentStart": 0,
          "currentEnd": 0,
          "sliceStart": 0,
        }
    axios
        .get('/channel/messages', {
          params: {
            token,
            channel_id: Number.parseInt(channel_id),
            start: p.isPaginating ? p.currentStart : 0,
          },
        })
        .then(({data}) => {
          const {messages: newMessages, start, end} = data;
          setPagination({ ...p, channelId: channel_id, currentEnd: end }); // TODO: add/remove problems
          setMessages(newMessages);
        })
        .catch((err) => {});
  }
  const step = useStep(fetchChannelMessages, [channel_id, pagination.currentStart]);

  const onPrev = () => setPagination(({sliceStart, currentStart, currentEnd, ...pagination}) => {

    const pageSize = messages.length;

    if (sliceStart + SLICE_SIZE < pageSize) {
      return {
        ...pagination,
        currentStart,
        currentEnd,
        sliceStart: sliceStart + SLICE_SIZE,
        isPaginating: true,
      };
    }

    return {
      ...pagination,
      currentEnd,
      currentStart: currentEnd,
      sliceStart: 0,
      isPaginating: true,
    };

  });

  const onNext = () => setPagination(({sliceStart, currentStart, ...pagination}) => {

    if (sliceStart >= SLICE_SIZE) {
      return {
        ...pagination,
        currentStart,
        sliceStart: sliceStart - SLICE_SIZE,
        isPaginating: !(currentStart == 0 && sliceStart == SLICE_SIZE)
      };
    }

    if (currentStart >= PAGINATION_SIZE) {
      if (currentStart) return {
        ...pagination,
        currentStart: currentStart - PAGINATION_SIZE,
        sliceStart: PAGINATION_SIZE-SLICE_SIZE,
      };
    }

    return {
      ...pagination,
      currentStart: 0,
      sliceStart: 0,
      isPaginating: false,
    };

  });

  const {currentStart, currentEnd, sliceStart, isPaginating} = pagination;

  const isEnd = currentEnd == -1 && sliceStart >= messages.length - SLICE_SIZE;

  const pinnedMessages = messages.filter(m => m.is_pinned);
  const subheader = !messages.length
      ? `Messages (None)`
      : `Messages [${currentStart+sliceStart+1}...${Math.min(currentStart+messages.length, currentStart+sliceStart+SLICE_SIZE)}]`;

  return (
    <StepProvider value={fetchChannelMessages}>
      {pinnedMessages.length > 0 && <>
        <hr />
        <List subheader={<ListSubheader>Pinned Messages</ListSubheader>}>
          {pinnedMessages.map(m => <Message key={m.message_id} {...m} />)}
        </List>
      </>}
      <hr />
      <List
        subheader={<ListSubheader>{subheader}</ListSubheader>}
        style={{ width: '100%' }}
      >
        {
          (!isEnd &&
            <ListItem>
              <Button
                variant="outlined"
                color="secondary"
                onClick={onPrev}
              >
                Previous messages
              </Button>
            </ListItem>
          )
        }
        {messages.slice(sliceStart, sliceStart + SLICE_SIZE).reverse().map((message) => (
          <Message key={message.message_id} {...message} />
        ))}
        {
          (isPaginating &&
            <ListItem>
              <Button
                variant="outlined"
                color="secondary"
                onClick={onNext}
              >
                Next messages
              </Button>
            </ListItem>
          )
        }
      </List>
      <AddMessage channel_id={channel_id} />
    </StepProvider>
  );
}

export default ChannelMessages;
