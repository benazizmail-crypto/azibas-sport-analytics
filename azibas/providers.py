"""Interfaces pour fournisseurs externes. Aucun fournisseur live n'est activé sans clés."""
from abc import ABC, abstractmethod

class SportsDataProvider(ABC):
    @abstractmethod
    def get_events(self, sport, date_from, date_to):
        raise NotImplementedError

class OddsProvider(ABC):
    @abstractmethod
    def get_odds(self, event_ids):
        raise NotImplementedError

class ProviderNotConfigured(RuntimeError):
    pass

class DisabledSportsDataProvider(SportsDataProvider):
    def get_events(self, sport, date_from, date_to):
        raise ProviderNotConfigured("Fournisseur de calendriers/statistiques non configuré.")

class DisabledOddsProvider(OddsProvider):
    def get_odds(self, event_ids):
        raise ProviderNotConfigured("Fournisseur de cotes non configuré.")
