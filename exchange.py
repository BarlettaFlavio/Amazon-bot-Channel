EXCHANGE=1.125

def from_usd_to_eur(usd):
	return usd/EXCHANGE

def from_eur_to_usd(eur):
	return EXCHANGE*eur