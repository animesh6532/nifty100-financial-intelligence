from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class PartnerRateThrottle(UserRateThrottle):
    scope = 'partner'
    THROTTLE_RATES = {
        'partner': '1000/day',
        'anon': '100/day',
    }


class AnonPartnerThrottle(AnonRateThrottle):
    scope = 'anon'
