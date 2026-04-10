// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DroneRegistry {

    // ========== REGISTRE D'IDENTITES ==========

    mapping(string => bool) public authorizedDrones;
    mapping(string => string) public dronePublicKeys;
    mapping(string => uint256) public droneRegistrationTime;

    function registerDrone(string memory droneId, string memory pubKey) public {
        authorizedDrones[droneId] = true;
        dronePublicKeys[droneId] = pubKey;
        droneRegistrationTime[droneId] = block.timestamp;

        _logInternally(droneId, "REGISTRATION", "Drone enregistre sur la blockchain");
        emit DroneRegistered(droneId, block.timestamp);
    }

    function isAuthorized(string memory droneId) public view returns (bool) {
        return authorizedDrones[droneId];
    }

    function getPublicKey(string memory droneId) public view returns (string memory) {
        return dronePublicKeys[droneId];
    }

    function revokeDrone(string memory droneId) public {
        authorizedDrones[droneId] = false;

        _logInternally(droneId, "REVOCATION", "Drone revoque");
        emit DroneRevoked(droneId, block.timestamp);
    }

    // ========== JOURNAL D'AUDIT ==========

    struct AuditEvent {
        string droneId;
        string eventType;
        uint256 timestamp;
        string details;
    }

    AuditEvent[] public auditLog;
    mapping(string => uint256[]) private droneEventIndices;

    // fonction interne utilisee par les autres fonctions
    function _logInternally(
        string memory droneId,
        string memory eventType,
        string memory details
    ) internal {
        AuditEvent memory newEvent = AuditEvent({
            droneId: droneId,
            eventType: eventType,
            timestamp: block.timestamp,
            details: details
        });

        uint256 index = auditLog.length;
        auditLog.push(newEvent);
        droneEventIndices[droneId].push(index);

        emit EventLogged(droneId, eventType, block.timestamp, details);
    }

    // connexion d'un drone (appele apres M3)
    function logConnection(string memory droneId) public {
        require(authorizedDrones[droneId], "Drone non autorise");
        _logInternally(droneId, "CONNECTION", "Session etablie apres handshake M1-M2-M3");
    }

    // rafraichissement de la cle de session K_DE
    function logKeyRefresh(
        string memory droneId,
        string memory sessionTokenHash
    ) public {
        require(authorizedDrones[droneId], "Drone non autorise");

        string memory details = string(abi.encodePacked(
            "KEY_REFRESH | token_hash:", sessionTokenHash
        ));

        _logInternally(droneId, "KEY_REFRESH", details);
    }

    // deconnexion d'un drone
    function logDisconnection(string memory droneId) public {
        require(authorizedDrones[droneId], "Drone non autorise");
        _logInternally(droneId, "DISCONNECTION", "Session terminee");
    }

    // evenement generique
    function logEvent(
        string memory droneId,
        string memory eventType,
        string memory details
    ) public {
        require(authorizedDrones[droneId], "Drone non autorise");
        _logInternally(droneId, eventType, details);
    }

    // ========== CONSULTATION DU JOURNAL ==========

    function getEventCount(string memory droneId) public view returns (uint256) {
        return droneEventIndices[droneId].length;
    }

    function getTotalEvents() public view returns (uint256) {
        return auditLog.length;
    }

    function getEvent(uint256 index) public view returns (
        string memory droneId,
        string memory eventType,
        uint256 timestamp,
        string memory details
    ) {
        require(index < auditLog.length, "Index invalide");
        AuditEvent memory e = auditLog[index];
        return (e.droneId, e.eventType, e.timestamp, e.details);
    }

    function getDroneEvents(string memory droneId) public view returns (uint256[] memory) {
        return droneEventIndices[droneId];
    }

    // ========== EVENEMENTS SOLIDITY ==========

    event DroneRegistered(string droneId, uint256 timestamp);
    event DroneRevoked(string droneId, uint256 timestamp);
    event EventLogged(string droneId, string eventType, uint256 timestamp, string details);
}