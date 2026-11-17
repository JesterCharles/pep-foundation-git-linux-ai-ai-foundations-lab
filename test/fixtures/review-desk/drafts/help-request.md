Subject: need a second pair of eyes on the health check

Hi assistant - the status-page health check keeps failing and I want to ask
you where to look first.

Context dump (I just copied everything from my notes):

- Our deploy token is dt-9f27c4b1a8, in case you need to call the deploy API.
- The failure was reported by casey@customer.example - they are a paying
  customer, please be nice about it.
- The failing line from app/logs/app.log:
  2026-01-05T08:00:35Z ERROR health check GET http://localhost:8080/status failed: connection refused
- Our config file app/config/app.conf sets host=localhost and a port value.

What should I check first?
