import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

secret = {
  "type": "service_account",
  "project_id": "hackathon-3f738",
  "private_key_id": "2173c9024048e82f69182252690bca8269dc2705",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC3pBWpQ2SDiyJ3\nZDgoxeHNMDnzpQUUVLJ+oVWAf+5Nj9AIR72uoF2v4QLjpsaUbWkJ5EeORuNz/ruQ\nIMxFcr8b48uMZ9BoYbDi8ninCv41O3s20ffYJugf2zvGVPxpMBVZ+CKUcVpbTwOq\nIDCuZkxNFcl1ZrZKwdSwTN2T+4yN52CUjjRLe58Zdg6H8fRPSB4LIZJnLkEDF9F9\nhQyKNV/VYuV4rKCtf3bDtOAmkM+2xAByF6Q0g7xLAjvvwruOj/6cVXldv2FBzyC5\nFGBW8WEOpDUh5hxCHprgbwinSQh5NE2byzfu24UhURaejEnoqLIU1gEOB37TNpQ1\n44A/CtdhAgMBAAECggEADi5wscqPh40GE1w87gEiB9tyjjsvIjvMMPU6ihrXB0xU\nz17i6gpeUce5lmT5rtqoIuhrEjStOfbw+xddTvumgHvd6zDVKkppA42f/Z5etTOr\ntzcNwbZ3dIZUnmNPvrvE2lbMLNR4GtcGPGwR9lXWDJnjHdrZtvoy945oChaB6y9S\nV8JfZRopTir5VvB+cCUbh4ZKugAZkT8rFPoTY0R93McyovxyNdR3mmNrZ9m5PfWw\nAMHU5MJ3oPCGXxtY4t0kvzUj7y+dhcbscbA9/HexvBL8peTgScAou7uY4cwjyS7H\nV5ND6yZDdPdCEqTr6WrpGIOtwrg9CRY6C1bnKdlu5QKBgQDyIcJ8WPlH+gzsebuB\nFbjJ/oXGYlM6seEq8+ags9Hbs35QMAzQgzZT8x05YqaNWurikIKtBfRcA3A9iHPc\nU4hWT2sz1rmeT/ieuJsEU7rONHyyddt9fbjZRPpkeN61FdhzN18aqk6tMApz/bav\nRSvE25kGQxBc8dPD0uaROpieiwKBgQDCKLTL9EBcECvNB7IoIKU/Rz5BqPSKUjAb\n1Pq3cQbXeraiBXItbRJIQOKgLQUQP0W4Vr2AB33nxULQ2NSQG7e0n/pZiq/v5Jz7\n4CrfCXN3GAgC59rCcm46zy9psAHxmFdTHaBKd8gLoGiGGr1L0DZWahzYejwwvD6w\n8jDbWmgrQwKBgC1X9yT0QJKjGCJ81Ylh+P4S5Rh2t2FpiGJT1J/JrQY4wfHgXbX6\nrITiJVnmyIv2N8CAEYi3ccB9gFp1oETle8W2D7xgfNhR35xRs+4GhBgzqhp9icIh\ndilyCnYgUIyW77b76pqCxEMYmQyJudlu2bh+61RJ4NmXC/JDH5yY3ZXrAoGARBqb\nMF9ApApYEtb8Ou8Yh5Wp1MY64Lnrfhe6ydWvnK3Cmhpm7mAv5YA8/gpMmGJZRkvG\ntL3r//xFb5RfGx1d1tG2sunexLrgBcmfwBREmCWpybsiFMqmt6Is81l1lRTmrJTb\nwMM7PDjL8R43//vM04rtC1H1AvNE2jRZxtdzapkCgYAsFW4Se9xt3sfZX8/5K1SY\nyt+F4QCtlqVZpmoqq50uj6pSXt8HLdBkUbKA6J+L9sJgVMuoD7mpvf2h+jAaI3el\njw4DvMzLItDnl0XP3CXpPmdtAkqPNvTtdY1BYlhWTjhA7YM4gW5Ae+vtWmWdD/JN\nij+zML74C0Y6WPE1salv7A==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-hqzs5@hackathon-3f738.iam.gserviceaccount.com",
  "client_id": "117838156090407506373",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-hqzs5%40hackathon-3f738.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

# secret = json.loads(os.getenv('FIREBASE_SERVICE_KEY'))
cred = credentials.Certificate(secret)
app = firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client(app)