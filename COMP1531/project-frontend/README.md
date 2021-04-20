# How to run the frontend

## The simple way

```bash
python3 frontend.py [BACKEND PORT]
```

For example:

```bash
python3 frontend.py 5000
```

The backend port is just an integer that is the port the flask server is CURRENTLY running on.

## The complex way

Only complete this step if you're comfortable self-teaching yourself ReactJS.

Run this once on the machine.
```bash
npm install
```

Start up your backend on a specific port.

Update `public/config.js` to use the correct backend port.

Then run:
```bash
npm start
```
