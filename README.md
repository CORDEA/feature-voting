# feature-voting

## Set up

### Development

```sh
$ npx wrangler d1 execute feature-voting-dev --local --file=./schema.sql
$ npx wrangler dev
```

### Production

```sh
$ npx wrangler login
$ npx wrangler d1 create feature-voting-dev
$ npx wrangler d1 list
$ npx wrangler deploy
```
